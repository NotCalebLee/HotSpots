#!/usr/bin/env python3
"""
Dartmouth Campus Heatmap - Interactive Visualization Generator
===============================================================

This script generates an interactive HTML heatmap visualization of Dartmouth
campus showing access point distribution (hotspots).

Input:  data/building_locations_processed.csv (cleaned building data)
        new-dartmouth-campus-map.png (campus map background)
Output: interactive_campus_heatmap.html (interactive visualization)

Features:
- Interactive tooltips showing building details on hover
- Color-coded by activity (red-yellow spectrum)
- Bubble size represents number of access points
- Zoom controls for detailed exploration
- Toggle heatmap mode for glow effect visualization
"""

import pandas as pd
import json
from pathlib import Path
import base64


def load_processed_data(csv_file):
    """Load the processed building location data."""
    print(f"📂 Loading processed data from {csv_file}...")
    df = pd.read_csv(csv_file)
    print(f"   Loaded {len(df)} buildings")
    return df


def encode_campus_map_image(image_path):
    """Encode campus map image as base64 for embedding in HTML."""
    print(f"🖼️  Encoding campus map image...")
    with open(image_path, 'rb') as f:
        image_data = f.read()
    encoded = base64.b64encode(image_data).decode('utf-8')
    print(f"   Image encoded ({len(encoded)} characters)")
    return f"data:image/png;base64,{encoded}"


def generate_html(df, map_image_base64, output_file):
    """Generate the interactive HTML heatmap."""
    
    print(f"🎨 Generating interactive HTML...")
    
    # Convert dataframe to JSON for JavaScript
    buildings_json = df.to_json(orient='records')
    
    # Get statistics for color scaling
    min_activity = int(df['num_access_points'].min())
    max_activity = int(df['num_access_points'].max())
    
    # HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dartmouth Campus Interactive Heatmap</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            color: #e0e0e0;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.1em;
        }}
        
        .controls {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .button-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        button {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .btn-primary {{
            background: #2a5298;
            color: white;
        }}
        
        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
        }}
        
        .btn-toggle {{
            background: #ff6b6b;
            color: white;
        }}
        
        .btn-toggle.active {{
            background: #51cf66;
        }}
        
        .canvas-container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            overflow: hidden;
            position: relative;
        }}
        
        canvas {{
            display: block;
            width: 100%;
            height: auto;
            cursor: crosshair;
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            pointer-events: none;
            display: none;
            z-index: 1000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        
        .tooltip-title {{
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 8px;
            color: #ffd700;
        }}
        
        .tooltip-info {{
            font-size: 14px;
            line-height: 1.6;
        }}
        
        .legend {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        
        .legend-title {{
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .legend-items {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            font-size: 14px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            border: 1px solid #333;
        }}
        
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #2a5298;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🗺️ Dartmouth Campus Access Point Heatmap</h1>
        <p class="subtitle">Interactive visualization of WiFi access point distribution across campus (circa 2014)</p>
        
        <div class="controls">
            <div class="button-group">
                <button class="btn-primary" onclick="zoomIn()">🔍 Zoom In</button>
                <button class="btn-primary" onclick="zoomOut()">🔍 Zoom Out</button>
                <button class="btn-secondary" onclick="resetZoom()">↺ Reset View</button>
            </div>
            <div class="button-group">
                <button class="btn-toggle" id="heatmapToggle" onclick="toggleHeatmap()">
                    Toggle Heatmap Mode
                </button>
            </div>
        </div>
        
        <div class="canvas-container">
            <canvas id="campusMap"></canvas>
            <div class="tooltip" id="tooltip">
                <div class="tooltip-title" id="tooltipTitle"></div>
                <div class="tooltip-info" id="tooltipInfo"></div>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-title">📊 Access Point Activity Legend</div>
            <div class="legend-items">
                <div class="legend-item">
                    <div class="legend-color" style="background: #ffff00;"></div>
                    <span>1-5 APs (Low Activity)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ffcc00;"></div>
                    <span>6-10 APs (Medium-Low)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff9900;"></div>
                    <span>11-15 APs (Medium)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff6600;"></div>
                    <span>16-20 APs (Medium-High)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff0000;"></div>
                    <span>20+ APs (High Activity)</span>
                </div>
            </div>
        </div>
        
        <div class="stats">
            <div class="legend-title">📈 Dataset Statistics</div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{len(df)}</div>
                    <div class="stat-label">Buildings</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{df['num_access_points'].sum()}</div>
                    <div class="stat-label">Total Access Points</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{df['num_access_points'].mean():.1f}</div>
                    <div class="stat-label">Avg APs per Building</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{df['num_access_points'].max()}</div>
                    <div class="stat-label">Max APs (Hottest Spot)</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Data
        const buildings = {buildings_json};
        const minActivity = {min_activity};
        const maxActivity = {max_activity};
        
        // Canvas setup
        const canvas = document.getElementById('campusMap');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        
        // State
        let scale = 1;
        let offsetX = 0;
        let offsetY = 0;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let heatmapMode = false;
        
        // Load campus map image
        const img = new Image();
        img.src = '{map_image_base64}';
        img.onload = () => {{
            canvas.width = img.width;
            canvas.height = img.height;
            draw();
        }};
        
        // Color function (red-yellow spectrum)
        function getColor(activity) {{
            const normalized = (activity - minActivity) / (maxActivity - minActivity);
            const red = 255;
            const green = Math.round(255 * (1 - normalized));
            const blue = 0;
            return `rgb(${{red}}, ${{green}}, ${{blue}})`;
        }}
        
        // Drawing function
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.save();
            
            // Apply transformations
            ctx.translate(offsetX, offsetY);
            ctx.scale(scale, scale);
            
            // Draw campus map
            ctx.globalAlpha = heatmapMode ? 0.4 : 0.9;
            ctx.drawImage(img, 0, 0);
            ctx.globalAlpha = 1.0;
            
            // Draw buildings
            buildings.forEach(building => {{
                const x = building.map_pixel_x;
                const y = building.map_pixel_y;
                const activity = building.num_access_points;
                const color = getColor(activity);
                const radius = Math.max(8, Math.min(30, 5 + activity * 1.5));
                
                // Heatmap glow effect
                if (heatmapMode) {{
                    const glowRadius = radius * 4;
                    const gradient = ctx.createRadialGradient(x, y, 0, x, y, glowRadius);
                    const normalized = (activity - minActivity) / (maxActivity - minActivity);
                    const red = 255;
                    const green = Math.round(255 * (1 - normalized));
                    
                    gradient.addColorStop(0, `rgba(${{red}}, ${{green}}, 0, 0.8)`);
                    gradient.addColorStop(0.4, `rgba(${{red}}, ${{green}}, 0, 0.4)`);
                    gradient.addColorStop(0.7, `rgba(${{red}}, ${{green}}, 0, 0.15)`);
                    gradient.addColorStop(1, `rgba(${{red}}, ${{green}}, 0, 0)`);
                    
                    ctx.fillStyle = gradient;
                    ctx.fillRect(x - glowRadius, y - glowRadius, glowRadius * 2, glowRadius * 2);
                }}
                
                // Draw building marker
                ctx.beginPath();
                ctx.arc(x, y, radius, 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
                ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
                ctx.lineWidth = 2;
                ctx.stroke();
            }});
            
            ctx.restore();
        }}
        
        // Zoom functions
        function zoomIn() {{
            scale *= 1.2;
            draw();
        }}
        
        function zoomOut() {{
            scale /= 1.2;
            draw();
        }}
        
        function resetZoom() {{
            scale = 1;
            offsetX = 0;
            offsetY = 0;
            draw();
        }}
        
        function toggleHeatmap() {{
            heatmapMode = !heatmapMode;
            document.getElementById('heatmapToggle').classList.toggle('active');
            draw();
        }}
        
        // Mouse events
        canvas.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left - offsetX) / scale;
            const y = (e.clientY - rect.top - offsetY) / scale;
            
            let hoveredBuilding = null;
            buildings.forEach(building => {{
                const dx = x - building.map_pixel_x;
                const dy = y - building.map_pixel_y;
                const radius = Math.max(8, Math.min(30, 5 + building.num_access_points * 1.5));
                if (Math.sqrt(dx*dx + dy*dy) < radius) {{
                    hoveredBuilding = building;
                }}
            }});
            
            if (hoveredBuilding) {{
                tooltip.style.display = 'block';
                tooltip.style.left = e.clientX + 15 + 'px';
                tooltip.style.top = e.clientY + 15 + 'px';
                document.getElementById('tooltipTitle').textContent = hoveredBuilding.BuildingName;
                document.getElementById('tooltipInfo').innerHTML = `
                    <strong>Code:</strong> ${{hoveredBuilding.BuildingCode}}<br>
                    <strong>Type:</strong> ${{hoveredBuilding.BuildingType}}<br>
                    <strong>Access Points:</strong> ${{hoveredBuilding.num_access_points}}<br>
                    <strong>Coordinates:</strong> (${{hoveredBuilding.map_pixel_x}}, ${{hoveredBuilding.map_pixel_y}})
                `;
            }} else {{
                tooltip.style.display = 'none';
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => {{
            tooltip.style.display = 'none';
        }});
    </script>
</body>
</html>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Interactive heatmap generated: {output_file}")
    print(f"   Total buildings visualized: {len(df)}")
    print(f"   Activity range: {min_activity}-{max_activity} APs")


def main():
    """Generate the interactive heatmap visualization."""
    
    print("=" * 70)
    print("DARTMOUTH CAMPUS HEATMAP - VISUALIZATION GENERATOR")
    print("=" * 70)
    
    # Load processed data
    df = load_processed_data('data/building_locations_processed.csv')
    
    # Encode campus map image
    map_image = encode_campus_map_image('new-dartmouth-campus-map.png')
    
    # Generate HTML
    generate_html(df, map_image, 'interactive_campus_heatmap.html')
    
    print("\n🎉 SUCCESS! Open 'interactive_campus_heatmap.html' in your browser.")
    print("=" * 70)


if __name__ == '__main__':
    main()

