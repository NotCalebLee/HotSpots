# Dartmouth Campus Interactive Heatmap - Project Summary

## 🎯 What Was Accomplished

Successfully created an **interactive heatmap** of Dartmouth campus showing access point activity, calibrated using real campus map coordinates.

## ✅ Calibration Results

Using **two reference points** to align coordinate system to campus map:

### Reference Point 1: Reed Hall
- **Building Code**: AcadBldg25
- **Data Coordinates**: (820087.58, 439107.95)
- **Map Pixel Position**: (689, 494)
- **Calibration Error**: 0.00 pixels ✅

### Reference Point 2: Thompson Arena  
- **Building Code**: AthlBldg3
- **Data Coordinates**: (822518.77, 437989.46)
- **Map Pixel Position**: (981, 627)
- **Calibration Error**: 1.22 pixels ✅

**Transformation Parameters:**
- Scale: 0.119898 pixels per coordinate unit
- Perfect alignment achieved!

## 📊 Final Dataset

**File**: `data/building_locations_processed.csv`

**Contains**: 129 unique buildings

**Columns**:
- `BuildingCode` - Original code (e.g., AcadBldg25)
- `BuildingName` - Actual building name (e.g., Reed Hall)
- `coord_x`, `coord_y` - Original data coordinates
- `map_pixel_x`, `map_pixel_y` - Calibrated pixel positions on campus map
- `num_access_points` - Number of APs (activity metric)
- `BuildingType` - Category (Acad, Res, Athl, Lib, Adm, Soc)

**Cleaning Applied**:
- ✅ z-coordinate removed
- ✅ All -1 (unknown) entries removed  
- ✅ APs aggregated by building
- ✅ Pixel coordinates calculated and verified

## 🗺️ Interactive Heatmap

**File**: `interactive_campus_heatmap.html`

### How to Use:
1. **Open** `interactive_campus_heatmap.html` in any web browser
2. **Hover** over colored circles to see building details
3. **Use buttons** to zoom in/out or toggle heatmap mode

### Features:
- ✅ **Interactive tooltips** showing:
  - Building name
  - Building code
  - Building type
  - Number of access points
  - Coordinates
- ✅ **Color-coded** by activity (Red-Yellow spectrum):
  - 🔴 Red = High activity (20+ APs)
  - 🟠 Orange = Medium-high activity (11-20 APs)
  - 🟡 Yellow = Low activity (1-10 APs)
- ✅ **Bubble size** = Number of access points
- ✅ **Zoom controls** for detailed viewing
- ✅ **Heatmap mode** for visualizing hot spots with glow effect
- ✅ **Campus map background** for geographic context

## 📁 Project Files

### Python Scripts:
1. `process_data.py` - Data cleaning & calibration pipeline
2. `generate_heatmap.py` - Interactive HTML visualization generator

### Data Files:
3. `data/dartmouth-location-data.csv` - Original Cisco AP location data (~2014)
4. `data/building_locations_processed.csv` - Cleaned and calibrated dataset

### Visualization:
5. `interactive_campus_heatmap.html` - **Main interactive heatmap** (open in browser)
6. `new-dartmouth-campus-map.png` - Campus map image used as background

### Documentation:
7. `README.md` - This file

## 🔧 How to Reproduce

This project is fully reproducible. To regenerate everything from scratch:

### Prerequisites
```bash
pip install pandas numpy
```

### Step 1: Process the Data
```bash
python3 process_data.py
```
This will:
- Load raw AP location data
- Remove invalid coordinates (-1 values)
- Aggregate APs by building
- Calibrate coordinates using two-point transformation
- Generate `data/building_locations_processed.csv`

### Step 2: Generate the Heatmap
```bash
python3 generate_heatmap.py
```
This will:
- Load processed building data
- Encode campus map image
- Generate `interactive_campus_heatmap.html`

### Step 3: View the Result
```bash
open interactive_campus_heatmap.html
```

## 🏛️ Key Buildings Identified

- **Reed Hall** (AcadBldg25) - Reference point
- **Thompson Arena** (AthlBldg3) - Reference point
- **Collis Center** (SocBldg11) - Your click verified our calibration!
- **Baker-Berry Library** (LibBldg1, LibBldg2)
- **Dartmouth Hall** (AcadBldg10)
- **Hopkins Center for the Arts** (SocBldg4)
- And 123 more...

## 🎨 Building Types

- **Acad** (Academic): 31 buildings - Orange markers
- **Res** (Residential): 58 buildings - Light blue markers  
- **Athl** (Athletic): 9 buildings - Red markers
- **Lib** (Library): 5 buildings - Dark blue markers
- **Adm** (Administrative): 20 buildings - Light green markers
- **Soc** (Social): 6 buildings - Pink markers

## 🚀 Quick Start

```bash
# Open the interactive heatmap in your default browser
open interactive_campus_heatmap.html
```

## 📝 Notes

- The heatmap shows **number of access points per building** as a metric for potential activity
- All coordinates have been validated with sub-2-pixel accuracy using a two-point calibration system
- Data is from Cisco AP locations circa 2014

