# wifi_pipeline.py
# End-to-end Wi-Fi placement pipeline using Dartmouth + HK references.
# Order: GPS -> RSSI+floor -> floor-only -> unplaced
# Adds source + confidence, time-windowing, dedupe, and remaps all timestamps to Jan 2015.

import math
import hashlib
import calendar
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import numpy as np
import pandas as pd


# =============================================================================
# PATHS (edit if your files are elsewhere)
# =============================================================================
ROOT = Path(r"C:\Users\lunes\Documents\Wifi-map")

# Dartmouth references
DART_APLOC_PATH = ROOT / "APlocations.csv"                   # AP → floor, local x/y
DART_AGG_PATH   = ROOT / "dartmouth_movement_agg_demo.csv"   # floor/day aggregate

# Hong Kong reference (Jan 2021)
HK_RAW_PATH     = ROOT / "202101-wifi-raw.csv"

# Outputs
OUT_DIR         = ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Synthetic coordinates (deterministic placement inside a bbox)
# =============================================================================
def _hash_u01(key: str) -> float:
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return (int(h[:8], 16) % 10_000_000) / 10_000_000.0

def synthetic_point(label: str,
                    bbox: Tuple[float, float, float, float],
                    floor: Optional[int] = None,
                    floor_jitter_deg: float = 0.0003) -> Tuple[float, float]:
    """
    Return (lat, lon) inside bbox=(lat_min, lat_max, lon_min, lon_max).
    Deterministic per label; small jitter per floor to avoid overlap.
    """
    lat_min, lat_max, lon_min, lon_max = bbox
    u = _hash_u01(label + "::lat")
    v = _hash_u01(label + "::lon")
    lat = lat_min + u * (lat_max - lat_min)
    lon = lon_min + v * (lon_max - lon_min)
    if floor is not None:
        fu = _hash_u01(f"{label}::floor::{floor}::u") - 0.5
        fv = _hash_u01(f"{label}::floor::{floor}::v") - 0.5
        lat += fu * floor_jitter_deg
        lon += fv * floor_jitter_deg
    return lat, lon


# =============================================================================
# RSSI utilities (used automatically if your data later includes signals)
# =============================================================================
def rssi_to_weight(rssi_dbm: float, floor_penalty_db: float = 0.0) -> float:
    """Convert RSSI (dBm) into a positive weight; clamps and soft-exponentials."""
    if pd.isna(rssi_dbm):
        return 0.0
    rssi = max(min(rssi_dbm, -30.0), -90.0) - floor_penalty_db
    k = 12.0
    return math.exp((rssi + 90.0) / k)

def estimate_from_rssi(signals: List[Dict[str, Any]],
                       ap_lookup: pd.DataFrame,
                       target_floor: Optional[int] = None) -> Optional[Dict[str, float]]:
    """
    Weighted centroid from AP coordinates using RSSI.
    signals: [{"ap": "AP_NAME", "rssi": -55}, ...]
    ap_lookup columns: ["AP","lat","lon","Floor"]
    """
    if not signals or ap_lookup is None or ap_lookup.empty:
        return None
    ap_map = ap_lookup.set_index("AP")[["lat", "lon", "Floor"]].to_dict(orient="index")
    w_sum = lat_sum = lon_sum = 0.0
    used = 0
    for s in signals:
        apid = s.get("ap"); rssi = s.get("rssi")
        if apid not in ap_map or rssi is None:
            continue
        lat = ap_map[apid]["lat"]; lon = ap_map[apid]["lon"]; ap_fl = ap_map[apid]["Floor"]
        if pd.isna(lat) or pd.isna(lon):
            continue
        penalty = 8.0 if (target_floor is not None and ap_fl != target_floor) else 0.0
        w = rssi_to_weight(rssi, penalty)
        lat_sum += w * lat; lon_sum += w * lon; w_sum += w; used += 1
    if used == 0 or w_sum == 0:
        return None
    return {"lat": lat_sum / w_sum, "lon": lon_sum / w_sum}


# =============================================================================
# Placement: GPS -> RSSI+floor -> floor-only -> unplaced
# =============================================================================
def place_point(row: pd.Series,
                ap_lookup: Optional[pd.DataFrame],
                floor_centroids: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """
    Returns {"lat","lon","floor","source","confidence"} for a record.
    """
    # 1) Exact GPS
    if "lat" in row and "lon" in row and pd.notna(row["lat"]) and pd.notna(row["lon"]):
        return dict(lat=row["lat"], lon=row["lon"],
                    floor=row.get("Floor", row.get("floor", np.nan)),
                    source="gps", confidence=1.0)

    # Normalize floor
    floor_val = row.get("Floor", row.get("floor", np.nan))
    fl = int(floor_val) if not pd.isna(floor_val) else None

    # 2) RSSI + floor
    signals = row.get("signals", None)
    if signals is not None and ap_lookup is not None and not ap_lookup.empty:
        est = estimate_from_rssi(signals, ap_lookup, target_floor=fl)
        if est is not None:
            return dict(lat=est["lat"], lon=est["lon"], floor=fl, source="rssi", confidence=0.7)

    # 3) Floor-only (use centroids)
    if fl is not None and floor_centroids is not None and not floor_centroids.empty:
        hit = floor_centroids.loc[floor_centroids["Floor"] == fl]
        if not hit.empty:
            base_lat = float(hit.iloc[0]["lat"]); base_lon = float(hit.iloc[0]["lon"])
            jitter = (hash((row.get("id", 0), fl)) % 1000) / 1e8  # tiny de-overlap
            return dict(lat=base_lat + jitter, lon=base_lon - jitter,
                        floor=fl, source="floor_only", confidence=0.3)

    # 4) Unplaced
    return dict(lat=np.nan, lon=np.nan, floor=fl, source="unplaced", confidence=0.0)


# =============================================================================
# Dartmouth: build AP lookup + floor centroids (synthetic lat/lon for now)
# =============================================================================
def build_dartmouth_ap_lookup(aplocations_csv: Path,
                              bbox_main: Tuple[float, float, float, float] = (43.7000, 43.7050, -72.2950, -72.2850)
                              ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      ap_lookup: [AP, Floor, lat, lon]
      floor_centroids: [Floor, lat, lon]
    Uses synthetic WGS84 positions within a bbox (deterministic) for prototyping.
    """
    ap = pd.read_csv(aplocations_csv).rename(columns={
        '#AP': 'AP',
        ' x coordinate (-1 = unknown)': 'x',
        ' y coordinate (-1 = unknown)': 'y',
        ' z coordinate (floor': 'floor_raw',
        ' 99 = unknown)': 'junk'
    })
    ap["Floor"] = pd.to_numeric(ap["floor_raw"], errors="coerce").astype("Int64")
    ap = ap.dropna(subset=["Floor"]).copy()
    ap["Floor"] = ap["Floor"].astype(int)

    lat_list, lon_list = [], []
    for _, r in ap.iterrows():
        lat, lon = synthetic_point(str(r["AP"]), bbox_main, floor=int(r["Floor"]))
        lat_list.append(lat); lon_list.append(lon)
    ap["lat"] = lat_list; ap["lon"] = lon_list

    floor_centroids = (ap.groupby("Floor", as_index=False)[["lat", "lon"]]
                         .mean()
                         .sort_values("Floor"))
    return ap[["AP", "Floor", "lat", "lon"]].copy(), floor_centroids


# =============================================================================
# Time windowing + dedup
# =============================================================================
def window_and_dedupe(df: pd.DataFrame,
                      ts_col: str = "timestamp",
                      device_col: str = "device_id",
                      window: str = "5T") -> pd.DataFrame:
    """
    Bucket into time windows and keep highest-confidence row per device per window.
    """
    out = df.copy()
    out["time_window"] = pd.to_datetime(out[ts_col]).dt.floor(window)
    out = out.sort_values([device_col, "time_window", "confidence"], ascending=[True, True, False])
    out = out.drop_duplicates([device_col, "time_window"], keep="first")
    return out


# =============================================================================
# Remap timestamps to a fixed month/year (Jan 2015 for both campuses)
# =============================================================================
def remap_to_month_year(df: pd.DataFrame, ts_col: str, year: int, month: int) -> pd.DataFrame:
    """Copy with timestamps remapped to given year/month, keeping day/time if possible."""
    df = df.copy()
    _, last_day = calendar.monthrange(year, month)
    ts = pd.to_datetime(df[ts_col])

    def _remap_one(t):
        day = min(t.day, last_day)
        return pd.Timestamp(year, month, day, t.hour, t.minute, t.second, t.microsecond)

    df[ts_col] = ts.apply(_remap_one)
    return df


# =============================================================================
# Pipeline
# =============================================================================
def run_pipeline():
    # ---------- Dartmouth: AP lookup (synthetic lat/lon) + floor centroids
    ap_lookup, floor_centroids = build_dartmouth_ap_lookup(DART_APLOC_PATH)

    # ---------- Dartmouth aggregate -> records
    dart = pd.read_csv(DART_AGG_PATH, parse_dates=["Date"])
    dart["Floor"] = pd.to_numeric(dart["Floor"], errors="coerce")
    dart = dart.dropna(subset=["Floor"]).copy()
    dart["Floor"] = dart["Floor"].astype(int)

    dart_records = (dart.rename(columns={"Date": "timestamp"})
                    [["timestamp", "Floor", "User-Count", "WiFi-Conn", "Duration-Sec"]]
                    .copy())

    dart_records = remap_to_month_year(dart_records, "timestamp", 2015, 1)

    dart_records["device_id"] = (
        "dart_f" + dart_records["Floor"].astype("Int64").astype("string") + "_" +
        dart_records["timestamp"].dt.date.astype("string")
    )

    # Place -> window/dedupe
    placed_dart = dart_records.apply(lambda r: place_point(r, ap_lookup, floor_centroids),
                                     axis=1).apply(pd.Series)
    dart_out = pd.concat([dart_records, placed_dart], axis=1)
    dart_clean = window_and_dedupe(dart_out, ts_col="timestamp", device_col="device_id", window="1D")

    # ---------- Hong Kong aggregate -> records
    # -------- Hong Kong aggregate
    hk = pd.read_csv(HK_RAW_PATH, parse_dates=["Date"])
    hk_agg = (hk.groupby(["Date", "Floor"], dropna=False)   # allow rows even if Floor is NaN
                .agg({"User-Count":"sum", "WiFi-Conn":"sum", "Duration-Sec":"sum"})
                .reset_index())

    # Force numeric; keep NaN if not numeric
    hk_agg["Floor"] = pd.to_numeric(hk_agg["Floor"], errors="coerce")

    # Drop rows with unknown floor (or choose to impute them)
    hk_agg = hk_agg.dropna(subset=["Floor"]).copy()

    # Now cast to int safely
    hk_agg["Floor"] = hk_agg["Floor"].astype(int)

    hk_records = (hk_agg.rename(columns={"Date": "timestamp"})
                        [["timestamp", "Floor", "User-Count", "WiFi-Conn", "Duration-Sec"]]
                        .copy())

    # Remap to Jan 2015
    hk_records = remap_to_month_year(hk_records, "timestamp", 2015, 1)

    # Create device_id without risking NaN
    hk_records["device_id"] = (
        "hk_f" + hk_records["Floor"].astype("Int64").astype("string") + "_" +
        hk_records["timestamp"].dt.date.astype("string")
    )


    # Place -> window/dedupe (HK has no APs/GPS; uses floor-only centroids from Dartmouth)
    placed_hk = hk_records.apply(lambda r: place_point(r, ap_lookup=None, floor_centroids=floor_centroids),
                                 axis=1).apply(pd.Series)
    hk_out = pd.concat([hk_records, placed_hk], axis=1)
    hk_clean = window_and_dedupe(hk_out, ts_col="timestamp", device_col="device_id", window="1D")

    # ---------- Save (all timestamps now in Jan 2015)
    dart_out.to_csv(OUT_DIR / "dartmouth_placed_raw_jan2015.csv", index=False)
    dart_clean.to_csv(OUT_DIR / "dartmouth_placed_windowed_dedup_jan2015.csv", index=False)
    hk_out.to_csv(OUT_DIR / "hk_placed_raw_jan2015.csv", index=False)
    hk_clean.to_csv(OUT_DIR / "hk_placed_windowed_dedup_jan2015.csv", index=False)

    # Quick campus totals (both Jan 2015)
    d_jan15 = dart_clean.copy(); d_jan15["Campus"] = "Main (Dartmouth 2015-01)"
    h_jan15 = hk_clean.copy();   h_jan15["Campus"] = "Sub (HongKong 2015-01)"
    both = pd.concat([d_jan15, h_jan15], ignore_index=True)

    monthly_totals = (both.groupby("Campus", as_index=False)
                           .agg(User_Count=("User-Count","sum"),
                                WiFi_Conn=("WiFi-Conn","sum"),
                                Duration_Sec=("Duration-Sec","sum")))
    monthly_totals.to_csv(OUT_DIR / "jan2015_campus_monthly_totals.csv", index=False)

    print("Pipeline complete (dates remapped to Jan 2015).")
    for p in [
        OUT_DIR / "dartmouth_placed_raw_jan2015.csv",
        OUT_DIR / "dartmouth_placed_windowed_dedup_jan2015.csv",
        OUT_DIR / "hk_placed_raw_jan2015.csv",
        OUT_DIR / "hk_placed_windowed_dedup_jan2015.csv",
        OUT_DIR / "jan2015_campus_monthly_totals.csv",
    ]:
        print(" -", p)


if __name__ == "__main__":
    run_pipeline()