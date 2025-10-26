#!/usr/bin/env python3
"""
Dartmouth Campus Heatmap - Data Processing Pipeline
====================================================

This script processes raw Cisco AP location data from Dartmouth campus (~2014)
and creates a cleaned, calibrated dataset with building-level aggregation.

Input:  data/dartmouth-location-data.csv (raw AP locations)
Output: data/building_locations_processed.csv (cleaned & calibrated)

Key Steps:
1. Load and clean raw data (remove invalid coordinates)
2. Aggregate access points by building
3. Calibrate coordinate system using two-point transformation
4. Map building codes to actual building names
5. Export final dataset for visualization
"""

import pandas as pd
import numpy as np
import re


# ============================================================================
# STEP 1: Data Cleaning
# ============================================================================

def clean_location_data(input_file):
    """
    Clean raw location data by removing invalid entries.
    
    Args:
        input_file: Path to raw dartmouth-location-data.csv
    
    Returns:
        DataFrame with cleaned data
    """
    print("📂 Loading raw data...")
    # CSV has descriptive column names, so we'll specify them explicitly
    df = pd.read_csv(input_file, 
                     names=['#AP', 'x', 'y', 'z'], 
                     skiprows=1,  # Skip header row
                     usecols=[0, 1, 2, 3])  # Only read first 4 columns
    print(f"   Original entries: {len(df)}")
    
    # Remove entries with unknown locations (-1 coordinates)
    df_clean = df[(df['x'] != -1) & (df['y'] != -1)].copy()
    print(f"   After removing invalid coordinates: {len(df_clean)}")
    
    # Drop z-coordinate (floor level not needed for 2D heatmap)
    df_clean = df_clean[['#AP', 'x', 'y']]
    
    return df_clean


# ============================================================================
# STEP 2: Building Aggregation
# ============================================================================

def extract_building_info(ap_name):
    """Extract building code and type from AP name."""
    # Example: "AcadBldg10AP13" -> ("AcadBldg10", "Acad")
    match = re.match(r'^([A-Za-z]+)Bldg(\d+)', ap_name)
    if match:
        building_type = match.group(1)
        building_num = match.group(2)
        building_code = f"{building_type}Bldg{building_num}"
        return building_code, building_type
    return None, None


def aggregate_by_building(df):
    """
    Aggregate access points by building.
    
    For each building:
    - Count number of APs
    - Average x,y coordinates across all APs
    """
    print("\n🏛️  Aggregating access points by building...")
    
    # Extract building codes
    df['BuildingCode'] = df['#AP'].apply(lambda x: extract_building_info(x)[0])
    df['BuildingType'] = df['#AP'].apply(lambda x: extract_building_info(x)[1])
    
    # Remove entries where building code couldn't be extracted
    df = df.dropna(subset=['BuildingCode'])
    
    # Aggregate by building
    building_df = df.groupby('BuildingCode').agg({
        'x': 'mean',
        'y': 'mean',
        'BuildingType': 'first',
        '#AP': 'count'
    }).reset_index()
    
    building_df.rename(columns={
        'x': 'coord_x',
        'y': 'coord_y',
        '#AP': 'num_access_points'
    }, inplace=True)
    
    print(f"   Unique buildings identified: {len(building_df)}")
    print(f"   Building types: {building_df['BuildingType'].unique()}")
    
    return building_df


# ============================================================================
# STEP 3: Coordinate Calibration (Two-Point Transformation)
# ============================================================================

def calibrate_coordinates(df):
    """
    Calibrate data coordinates to pixel coordinates on campus map.
    
    Uses two known reference points:
    - Reed Hall (AcadBldg25): (689, 494) on map
    - Thompson Arena (AthlBldg3): (981, 627) on map
    
    Map dimensions: 5100 x 3300 pixels
    """
    print("\n🎯 Calibrating coordinates using two-point transformation...")
    
    # Reference Point 1: Reed Hall
    reed_data_x = df[df['BuildingCode'] == 'AcadBldg25']['coord_x'].values[0]
    reed_data_y = df[df['BuildingCode'] == 'AcadBldg25']['coord_y'].values[0]
    reed_pixel_x = 689
    reed_pixel_y = 494
    
    # Reference Point 2: Thompson Arena
    thompson_data_x = df[df['BuildingCode'] == 'AthlBldg3']['coord_x'].values[0]
    thompson_data_y = df[df['BuildingCode'] == 'AthlBldg3']['coord_y'].values[0]
    thompson_pixel_x = 981
    thompson_pixel_y = 627
    
    print(f"   Reed Hall:       data=({reed_data_x:.2f}, {reed_data_y:.2f}) -> pixel=({reed_pixel_x}, {reed_pixel_y})")
    print(f"   Thompson Arena:  data=({thompson_data_x:.2f}, {thompson_data_y:.2f}) -> pixel=({thompson_pixel_x}, {thompson_pixel_y})")
    
    # Calculate linear transformation parameters
    # pixel = scale * data + offset
    scale_x = (thompson_pixel_x - reed_pixel_x) / (thompson_data_x - reed_data_x)
    offset_x = reed_pixel_x - (scale_x * reed_data_x)
    
    scale_y = (thompson_pixel_y - reed_pixel_y) / (thompson_data_y - reed_data_y)
    offset_y = reed_pixel_y - (scale_y * reed_data_y)
    
    print(f"   Scale: x={scale_x:.6f}, y={scale_y:.6f}")
    
    # Apply transformation to all buildings
    df['map_pixel_x'] = (df['coord_x'] * scale_x + offset_x).round().astype(int)
    df['map_pixel_y'] = (df['coord_y'] * scale_y + offset_y).round().astype(int)
    
    # Verify calibration accuracy
    reed_calc_x = df[df['BuildingCode'] == 'AcadBldg25']['map_pixel_x'].values[0]
    reed_calc_y = df[df['BuildingCode'] == 'AcadBldg25']['map_pixel_y'].values[0]
    thompson_calc_x = df[df['BuildingCode'] == 'AthlBldg3']['map_pixel_x'].values[0]
    thompson_calc_y = df[df['BuildingCode'] == 'AthlBldg3']['map_pixel_y'].values[0]
    
    reed_error = np.sqrt((reed_calc_x - reed_pixel_x)**2 + (reed_calc_y - reed_pixel_y)**2)
    thompson_error = np.sqrt((thompson_calc_x - thompson_pixel_x)**2 + (thompson_calc_y - thompson_pixel_y)**2)
    
    print(f"   Calibration error: Reed={reed_error:.2f}px, Thompson={thompson_error:.2f}px ✅")
    
    return df


# ============================================================================
# STEP 4: Building Name Mapping
# ============================================================================

def map_building_names(df):
    """
    Map building codes to actual building names.
    
    This mapping was derived from the campus map and calibration process.
    """
    print("\n🏢 Mapping building codes to actual names...")
    
    # Building name dictionary (based on campus map and pixel locations)
    building_names = {
        'AcadBldg25': 'Reed Hall',
        'AthlBldg3': 'Thompson Arena',
        'SocBldg11': 'Collis Center',
        'LibBldg1': 'Baker-Berry Library (Main)',
        'LibBldg2': 'Baker-Berry Library (Tower)',
        'AcadBldg10': 'Dartmouth Hall',
        'SocBldg4': 'Hopkins Center for the Arts',
        # Add more mappings as identified
    }
    
    # Apply known names, use code as fallback
    df['BuildingName'] = df['BuildingCode'].apply(
        lambda x: building_names.get(x, x)
    )
    
    print(f"   {len([k for k in df['BuildingName'] if k in building_names.values()])} buildings named")
    print(f"   {len(df) - len([k for k in df['BuildingName'] if k in building_names.values()])} buildings using code as name")
    
    return df


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    """Execute the complete data processing pipeline."""
    
    print("=" * 70)
    print("DARTMOUTH CAMPUS HEATMAP - DATA PROCESSING PIPELINE")
    print("=" * 70)
    
    # Step 1: Clean raw data
    df = clean_location_data('data/dartmouth-location-data.csv')
    
    # Step 2: Aggregate by building
    df = aggregate_by_building(df)
    
    # Step 3: Calibrate coordinates
    df = calibrate_coordinates(df)
    
    # Step 4: Map building names
    df = map_building_names(df)
    
    # Reorder columns for clarity
    df = df[[
        'BuildingCode',
        'BuildingName', 
        'BuildingType',
        'num_access_points',
        'coord_x',
        'coord_y',
        'map_pixel_x',
        'map_pixel_y'
    ]]
    
    # Save final dataset
    output_file = 'data/building_locations_processed.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ SUCCESS! Final dataset saved to: {output_file}")
    print(f"   Total buildings: {len(df)}")
    print(f"   Total access points: {df['num_access_points'].sum()}")
    print(f"   Activity range: {df['num_access_points'].min()}-{df['num_access_points'].max()} APs per building")
    print("=" * 70)
    
    return df


if __name__ == '__main__':
    df = main()
    print("\n📊 Sample of processed data:")
    print(df.head(10).to_string())

