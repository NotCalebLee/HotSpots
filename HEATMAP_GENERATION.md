# Heatmap Generation Instructions

This guide explains how to generate and use the Wi-Fi heatmap visualizations in your HotSpots app.

## Prerequisites

Make sure you have Python installed with the following packages:

```bash
pip install pandas matplotlib seaborn numpy
```

## Required Data Files

Your Python scripts expect these CSV files:

- `APlocations.csv` - Access Point locations for Dartmouth
- `dartmouth_movement_agg_demo.csv` - Dartmouth movement data
- `202101-wifi-raw.csv` - Hong Kong Wi-Fi data

Update the paths in `src/data/wifiProto.py` and `src/data/mapHeats.py` to match your file locations.

## Generate Heatmaps

### Option 1: Use the convenience script (Recommended)

```bash
python generate_heatmaps.py
```

### Option 2: Run the scripts manually

1. **Generate the data**:

```bash
cd src/data
python wifiProto.py
```

2. **Generate the heatmap images**:

```bash
python mapHeats.py
```

This will create:

- `dart_heatmap.png` - Dartmouth Wi-Fi heatmap
- `hk_heatmap.png` - Hong Kong Wi-Fi heatmap
- `hk_3d_heatmap.png` - Hong Kong 3D building heatmap

## Copy Images to React App

After generation, copy the images to your React assets folder:

```bash
# From your project root
cp outputs/dart_heatmap.png src/assets/
cp outputs/hk_heatmap.png src/assets/
```

## Update React Component

Once `hk_heatmap.png` is in your assets folder, update `src/components/About/About.tsx`:

```javascript
// Change this line:
import hkHeatmap from "../../assets/Heat-Map2.jpg";

// To:
import hkHeatmap from "../../assets/hk_heatmap.png";
```

## Viewing the Results

The heatmaps will automatically appear in the "Sample Data" section of your website at:

- **Dartmouth Wi-Fi Heat Map** - Left card
- **Hong Kong Wi-Fi Heat Map** - Right card

The visualizations show:

- Red intensity indicates higher Wi-Fi usage/density
- Scatter points show individual data points
- Coordinates are based on latitude/longitude

## Troubleshooting

**Issue**: File paths don't work

- **Solution**: Update the paths in `wifiProto.py` lines 19-27 to match your directory structure

**Issue**: Missing CSV files

- **Solution**: Make sure all required CSV files are in the correct location

**Issue**: Module not found errors

- **Solution**: Install required packages: `pip install pandas matplotlib seaborn numpy`

**Issue**: Images don't appear in the website

- **Solution**: Make sure images are copied to `src/assets/` and the import statements are correct

## Current Status

✅ **Dartmouth heatmap** - Already integrated (using `dart_heatmap.png`)
⏳ **Hong Kong heatmap** - Using placeholder (Heat-Map2.jpg) - Run the script to generate and replace
