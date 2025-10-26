"""
Quick script to generate heatmaps and copy them to React assets folder.
Run this script from the project root: python generate_heatmaps.py
"""
import sys
from pathlib import Path

# Add src/data to Python path
sys.path.insert(0, str(Path(__file__).parent / "src" / "data"))

try:
    # First, run the Wi-Fi processing pipeline to generate data
    print("Running Wi-Fi data processing pipeline...")
    import wifiProto
    wifiProto.run_pipeline()
    
    # Then generate the heatmaps from the processed data
    print("\nGenerating heatmaps...")
    import mapHeats
    
    print("\n✅ Heatmaps generated successfully!")
    print("📁 Check the outputs folder for generated images.")
    print("\n📋 Next steps:")
    print("1. Copy dart_heatmap.png to src/assets/")
    print("2. Copy hk_heatmap.png to src/assets/")
    print("3. Refresh your browser to see the updated visualizations")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Make sure you have the required CSV files:")
    print("   - APlocations.csv")
    print("   - dartmouth_movement_agg_demo.csv")
    print("   - 202101-wifi-raw.csv")

