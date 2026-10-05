import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

sys.path.insert(0, 'Source_Code')
from preprocessing.config import ROI_LONLAT, YEARS, START, END

os.makedirs('extracted_assets', exist_ok=True)

# -------------------------------------------------------------
# 1. STUDY AREA MAP: BARANGAY DULAO, ARINGAY, LA UNION
# -------------------------------------------------------------
def generate_study_area_map():
    coords = ROI_LONLAT
    lons = [pt[0] for pt in coords]
    lats = [pt[1] for pt in coords]

    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#E9ECEF')

    # Water background (Lingayen Gulf side to the west)
    ax.axhspan(min(lats)-0.01, max(lats)+0.01, facecolor='#D0E8F2', zorder=1)
    # Landmass polygon on the east
    ax.axvspan(min(lons)+0.008, max(lons)+0.02, facecolor='#E3EED4', zorder=2)

    # Plot Study Area ROI Polygon
    roi_poly = patches.Polygon(coords, closed=True, facecolor='#2D6A4F', edgecolor='#1B4332',
                               linewidth=2.5, alpha=0.45, zorder=5, label='Dulao Mangrove ROI (316.74 ha)')
    ax.add_patch(roi_poly)

    # Plot vertices
    ax.scatter(lons, lats, color='#1B4332', s=25, zorder=6, edgecolors='white', linewidth=1)

    # Annotations
    ax.text(120.358, 16.383, 'Barangay Dulao\nMangrove Zone\n(316.74 ha)',
            fontsize=11, fontweight='bold', color='#081C15', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85, edgecolor='#2D6A4F', lw=1.5),
            zorder=7)
    
    ax.text(min(lons) - 0.003, 16.380, 'Lingayen Gulf\n(South China Sea)',
            fontsize=10, fontstyle='italic', color='#1A5276', ha='center', va='center', zorder=4)

    ax.text(max(lons) + 0.004, 16.390, 'Aringay Mainland\n(Agricultural / Inland)',
            fontsize=9, fontstyle='italic', color='#4A5568', ha='center', va='center', zorder=4)

    # Coordinate extents & styling
    ax.set_xlim(min(lons) - 0.007, max(lons) + 0.009)
    ax.set_ylim(min(lats) - 0.005, max(lats) + 0.005)
    ax.set_title('Study Area: Barangay Dulao, Aringay, La Union\nROI Geographic Boundary (Sentinel-2 Footprint)', 
                 fontsize=12, fontweight='bold', pad=12, color='#1B4332')
    ax.set_xlabel('Longitude (°E)', fontsize=10, fontweight='bold', color='#2D3748')
    ax.set_ylabel('Latitude (°N)', fontsize=10, fontweight='bold', color='#2D3748')
    ax.grid(True, linestyle='--', alpha=0.5, color='#A0AEC0', zorder=3)

    # North arrow
    ax.annotate('N', xy=(0.92, 0.88), xytext=(0.92, 0.78),
                xycoords='axes fraction', ha='center', va='bottom',
                fontsize=12, fontweight='bold', color='#1B4332',
                arrowprops=dict(arrowstyle='->', facecolor='#1B4332', edgecolor='#1B4332', lw=2),
                zorder=10)

    # Metadata card in lower left
    info_text = "Spatial Coverage: 316.74 ha\nTarget Years: 2019–2024\nSeason: Dry (Feb 1 – Apr 30)\nSensor: Sentinel-2 MSI"
    ax.text(0.03, 0.05, info_text, transform=ax.transAxes, fontsize=8.5,
            bbox=dict(boxstyle='square,pad=0.5', facecolor='#FFFFFF', edgecolor='#CBD5E0', lw=1),
            zorder=10, verticalalignment='bottom')

    ax.legend(loc='upper left', framealpha=0.9, fontsize=9)
    plt.tight_layout()
    plt.savefig('extracted_assets/dulao_roi_map.png', dpi=300)
    plt.close()
    print("Generated extracted_assets/dulao_roi_map.png")

# -------------------------------------------------------------
# 2. FEATURE EXTRACTION & TENSOR PIPELINE DIAGRAM
# -------------------------------------------------------------
def generate_feature_pipeline():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    # Draw boxes
    boxes = [
        {"x": 0.02, "y": 0.25, "w": 0.16, "h": 0.5, "title": "Sentinel-2 MSI\nL2A Surface\nReflectance", "color": "#1A5276", "text": "Cloud < 20%\nFeb–Apr Dry Season\n(2019–2024)"},
        {"x": 0.24, "y": 0.15, "w": 0.22, "h": 0.7, "title": "Selected 4 Bands", "color": "#2D6A4F", "text": "• B3 (Green, 560nm, 10m)\n• B4 (Red, 665nm, 10m)\n• B8 (NIR, 842nm, 10m)\n• B11 (SWIR, 1610nm, 20m\n   → Bilinear to 10m)"},
        {"x": 0.52, "y": 0.25, "w": 0.20, "h": 0.5, "title": "Computed Feature\nNDVI", "color": "#1B4332", "text": "NDVI = (B8 - B4)\n       / (B8 + B4)\n\nNorm: [0, 1] range\nVegetation vigor"},
        {"x": 0.78, "y": 0.20, "w": 0.20, "h": 0.6, "title": "Stacked Tensor\nInput to U-Net", "color": "#B7791F", "text": "Shape:\n256 × 256 × 5\n\nChannels:\n[B3, B4, B8, B11, NDVI]\nNormalized [0, 1]"}
    ]

    for b in boxes:
        rect = patches.FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                                      boxstyle="round,pad=0.02,rounding_size=0.03",
                                      facecolor="#F7FAFC", edgecolor=b["color"], linewidth=2.5)
        ax.add_patch(rect)
        # Header banner inside box
        banner = patches.FancyBboxPatch((b["x"], b["y"] + b["h"] - 0.16), b["w"], 0.16,
                                        boxstyle="round,pad=0.02,rounding_size=0.03",
                                        facecolor=b["color"], edgecolor=b["color"], linewidth=1)
        ax.add_patch(banner)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 0.08, b["title"],
                ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)
        ax.text(b["x"] + 0.02, b["y"] + (b["h"] - 0.18)/2, b["text"],
                ha='left', va='center', color='#2D3748', fontsize=8.5, linespacing=1.3)

    # Arrows
    arrow_props = dict(facecolor='#4A5568', edgecolor='#4A5568', width=2, headwidth=8)
    ax.annotate('', xy=(0.23, 0.5), xytext=(0.19, 0.5), arrowprops=arrow_props)
    ax.annotate('', xy=(0.51, 0.5), xytext=(0.47, 0.5), arrowprops=arrow_props)
    ax.annotate('', xy=(0.77, 0.5), xytext=(0.73, 0.5), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig('extracted_assets/spectral_bands_ndvi_pipeline.png', dpi=300)
    plt.close()
    print("Generated extracted_assets/spectral_bands_ndvi_pipeline.png")

# -------------------------------------------------------------
# 3. TRANSITION MATRIX / CHANGE DETECTION FRAMEWORK
# -------------------------------------------------------------
def generate_transition_matrix():
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    # Draw Matrix grid
    ax.text(0.5, 0.92, "Post-Classification Comparison (PCC) Transition Matrix", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1B4332')
    ax.text(0.5, 0.84, "Pixel-by-Pixel Logic: Previous Year (T₁) → Current Year (T₂)", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#4A5568')

    classes = [
        {"x": 0.05, "y": 0.42, "w": 0.42, "h": 0.35, "title": "GAIN (Mangrove Expansion)", 
         "rule": "Previous: Non-Mangrove (0)  →  Current: Mangrove (1)", 
         "desc": "Natural colonization, estuarine progradation,\nor artificial mangrove reforestation planting.",
         "color": "#2D6A4F", "bg": "#E8F5E9"},
        {"x": 0.53, "y": 0.42, "w": 0.42, "h": 0.35, "title": "LOSS (Mangrove Deforestation)", 
         "rule": "Previous: Mangrove (1)  →  Current: Non-Mangrove (0)", 
         "desc": "Fishpond conversion, typhoon/storm surge scour,\ninfrastructure encroachment, or coastal harvesting.",
         "color": "#BA181B", "bg": "#FFEBEE"},
        {"x": 0.05, "y": 0.03, "w": 0.42, "h": 0.35, "title": "STABLE MANGROVE (Persistent)", 
         "rule": "Previous: Mangrove (1)  →  Current: Mangrove (1)", 
         "desc": "Healthy core mangrove canopy intact across\nboth observation years without disturbance.",
         "color": "#1B4332", "bg": "#E0F2F1"},
        {"x": 0.53, "y": 0.03, "w": 0.42, "h": 0.35, "title": "STABLE NON-MANGROVE (Unchanged)", 
         "rule": "Previous: Non-Mangrove (0)  →  Current: Non-Mangrove (0)", 
         "desc": "Open water (Lingayen Gulf, river channels), mudflats,\nagricultural land, or coastal sandy substrate.",
         "color": "#4A5568", "bg": "#F5F5F5"}
    ]

    for c in classes:
        rect = patches.FancyBboxPatch((c["x"], c["y"]), c["w"], c["h"],
                                      boxstyle="round,pad=0.02,rounding_size=0.03",
                                      facecolor=c["bg"], edgecolor=c["color"], linewidth=2.5)
        ax.add_patch(rect)
        ax.text(c["x"] + 0.03, c["y"] + c["h"] - 0.07, c["title"],
                ha='left', va='center', color=c["color"], fontweight='bold', fontsize=11)
        ax.text(c["x"] + 0.03, c["y"] + c["h"] - 0.16, c["rule"],
                ha='left', va='center', color='#1A202C', fontweight='bold', fontsize=9)
        ax.text(c["x"] + 0.03, c["y"] + 0.07, c["desc"],
                ha='left', va='center', color='#4A5568', fontsize=8.5, linespacing=1.2)

    plt.tight_layout()
    plt.savefig('extracted_assets/transition_matrix_diagram.png', dpi=300)
    plt.close()
    print("Generated extracted_assets/transition_matrix_diagram.png")

# -------------------------------------------------------------
# 4. SYSTEM ARCHITECTURE DIAGRAM
# -------------------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    ax.text(0.5, 0.94, "Three-Tier Prototype Software Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1B4332')

    layers = [
        {"x": 0.03, "w": 0.28, "color": "#1A5276", "title": "Data & Preprocessing",
         "items": ["• Sentinel-2 L2A Multispectral Assets", "• B3, B4, B8, B11 & NDVI Stack", "• 256×256 Patch Generator", "• Dulao 25-Point ROI GeoJSON", "• Reference Ground-Truth Labels"]},
        {"x": 0.36, "w": 0.28, "color": "#2D6A4F", "title": "Flask Backend & Engine",
         "items": ["• REST API Endpoints (/api/data, etc.)", "• U-Net Binary Inference Pipeline", "• PCC Transition Engine (Gain/Loss)", "• Summary Statistics Calculator", "• ReportLab Automated PDF Engine"]},
        {"x": 0.69, "w": 0.28, "color": "#B7791F", "title": "Interactive Client (Web UI)",
         "items": ["• Responsive HTML5 / Jinja2 Layout", "• Leaflet.js Interactive Web Map", "• Layer Toggles (Gain, Loss, ROI)", "• Chart.js Multi-Temporal Trends", "• One-Click Aringay MENRO PDF Export"]}
    ]

    for lyr in layers:
        rect = patches.FancyBboxPatch((lyr["x"], 0.15), lyr["w"], 0.70,
                                      boxstyle="round,pad=0.02,rounding_size=0.03",
                                      facecolor="#F8FAFC", edgecolor=lyr["color"], linewidth=2.5)
        ax.add_patch(rect)
        # Banner
        banner = patches.FancyBboxPatch((lyr["x"], 0.75), lyr["w"], 0.10,
                                        boxstyle="round,pad=0.02,rounding_size=0.03",
                                        facecolor=lyr["color"], edgecolor=lyr["color"], linewidth=1)
        ax.add_patch(banner)
        ax.text(lyr["x"] + lyr["w"]/2, 0.80, lyr["title"],
                ha='center', va='center', color='white', fontweight='bold', fontsize=10.5)

        y_pos = 0.65
        for item in lyr["items"]:
            ax.text(lyr["x"] + 0.02, y_pos, item, ha='left', va='center',
                    color='#2D3748', fontsize=8.5)
            y_pos -= 0.11

    # Connectors between tiers
    arrow_props = dict(facecolor='#4A5568', edgecolor='#4A5568', width=2, headwidth=8)
    ax.annotate('', xy=(0.35, 0.50), xytext=(0.32, 0.50), arrowprops=arrow_props)
    ax.annotate('', xy=(0.68, 0.50), xytext=(0.65, 0.50), arrowprops=arrow_props)

    # Note
    ax.text(0.5, 0.06, "Clean Decoupled Architecture: Flask Backend communicates via REST JSON with Leaflet/Chart.js Frontend",
            ha='center', va='center', color='#718096', fontsize=8.5, fontstyle='italic')

    plt.tight_layout()
    plt.savefig('extracted_assets/system_architecture_diagram.png', dpi=300)
    plt.close()
    print("Generated extracted_assets/system_architecture_diagram.png")

# -------------------------------------------------------------
# 5. HIGH-FIDELITY PROTOTYPE UI DASHBOARD VISUAL
# -------------------------------------------------------------
def generate_prototype_ui_mockup():
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=300)
    fig.patch.set_facecolor('#1A202C')
    ax.set_facecolor('#1A202C')
    ax.axis('off')

    # Top Navigation Bar
    navbar = patches.Rectangle((0, 0.90), 1, 0.10, facecolor='#111827', edgecolor='#374151', lw=1)
    ax.add_patch(navbar)
    ax.text(0.03, 0.95, "🌱 MANGROVE GAIN & LOSS DETECTION SYSTEM", color='#10B981', fontweight='bold', fontsize=11, va='center')
    ax.text(0.48, 0.95, "Barangay Dulao, Aringay, La Union (2019–2024)", color='#E5E7EB', fontsize=9.5, va='center')
    # Demo badge
    badge = patches.FancyBboxPatch((0.82, 0.92), 0.15, 0.06, boxstyle='round,pad=0.01', facecolor='#DC2626', edgecolor='white', lw=1)
    ax.add_patch(badge)
    ax.text(0.895, 0.95, "DEMO MODE", color='white', fontweight='bold', fontsize=8, ha='center', va='center')

    # Left Control Sidebar
    sidebar = patches.Rectangle((0.02, 0.05), 0.28, 0.82, facecolor='#1F2937', edgecolor='#374151', lw=1)
    ax.add_patch(sidebar)
    ax.text(0.04, 0.83, "ANALYSIS CONTROLS", color='#9CA3AF', fontweight='bold', fontsize=9)
    ax.text(0.04, 0.77, "Baseline Year (T₁): 2019", color='white', fontsize=8.5)
    ax.text(0.04, 0.72, "Comparison Year (T₂): 2024", color='white', fontsize=8.5)
    ax.text(0.04, 0.65, "Classification Threshold: 0.50", color='#A7F3D0', fontsize=8.5)

    # Metric Cards in Sidebar
    m1 = patches.FancyBboxPatch((0.04, 0.48), 0.24, 0.13, boxstyle='round,pad=0.01', facecolor='#064E3B', edgecolor='#059669', lw=1)
    ax.add_patch(m1)
    ax.text(0.06, 0.57, "Detected Gain (T₁ → T₂)", color='#A7F3D0', fontsize=7.5)
    ax.text(0.06, 0.51, "+3.20 ha  (Demo)", color='white', fontweight='bold', fontsize=11)

    m2 = patches.FancyBboxPatch((0.04, 0.32), 0.24, 0.13, boxstyle='round,pad=0.01', facecolor='#7F1D1D', edgecolor='#DC2626', lw=1)
    ax.add_patch(m2)
    ax.text(0.06, 0.41, "Detected Loss (T₁ → T₂)", color='#FECACA', fontsize=7.5)
    ax.text(0.06, 0.35, "-1.10 ha  (Demo)", color='white', fontweight='bold', fontsize=11)

    # PDF Button
    pdf_btn = patches.FancyBboxPatch((0.04, 0.12), 0.24, 0.08, boxstyle='round,pad=0.01', facecolor='#2563EB', edgecolor='white', lw=1)
    ax.add_patch(pdf_btn)
    ax.text(0.16, 0.16, "📄 Export MENRO PDF Report", color='white', fontweight='bold', fontsize=8, ha='center', va='center')

    # Main Map Viewport
    map_box = patches.Rectangle((0.32, 0.26), 0.66, 0.61, facecolor='#0F172A', edgecolor='#374151', lw=1)
    ax.add_patch(map_box)
    ax.text(0.34, 0.83, "Interactive Leaflet.js Cartographic Display", color='#94A3B8', fontsize=9, fontweight='bold')
    
    # Simulated coastline and patches
    ax.plot([0.45, 0.50, 0.58, 0.65, 0.72, 0.80], [0.35, 0.48, 0.55, 0.62, 0.70, 0.78], color='#38BDF8', lw=2, linestyle='--')
    # Mangrove patches
    g_patch = patches.Circle((0.55, 0.52), 0.04, facecolor='#10B981', alpha=0.7, edgecolor='white', lw=1)
    l_patch = patches.Circle((0.62, 0.58), 0.03, facecolor='#EF4444', alpha=0.8, edgecolor='white', lw=1)
    s_patch = patches.Circle((0.68, 0.65), 0.05, facecolor='#047857', alpha=0.6, edgecolor='white', lw=1)
    ax.add_patch(g_patch); ax.add_patch(l_patch); ax.add_patch(s_patch)
    ax.text(0.55, 0.52, "Gain", color='white', fontsize=7, ha='center', va='center', fontweight='bold')
    ax.text(0.62, 0.58, "Loss", color='white', fontsize=7, ha='center', va='center', fontweight='bold')
    ax.text(0.68, 0.65, "Stable", color='white', fontsize=7, ha='center', va='center', fontweight='bold')

    # Bottom Chart Panel
    chart_box = patches.Rectangle((0.32, 0.05), 0.66, 0.18, facecolor='#1E293B', edgecolor='#374151', lw=1)
    ax.add_patch(chart_box)
    ax.text(0.34, 0.20, "Multi-Temporal Mangrove Extent (2019–2024 Demo Trend)", color='#CBD5E1', fontsize=8, fontweight='bold')
    years_x = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
    vals_y =  [0.10, 0.12, 0.11, 0.14, 0.15, 0.17]
    ax.plot(years_x, vals_y, color='#10B981', marker='o', lw=2)
    for yx, label in zip(years_x, ['2019', '2020', '2021', '2022', '2023', '2024']):
        ax.text(yx, 0.07, label, color='#94A3B8', fontsize=7, ha='center')

    plt.tight_layout()
    plt.savefig('extracted_assets/prototype_ui_mockup.png', dpi=300)
    plt.close()
    print("Generated extracted_assets/prototype_ui_mockup.png")

if __name__ == '__main__':
    generate_study_area_map()
    generate_feature_pipeline()
    generate_transition_matrix()
    generate_system_architecture()
    generate_prototype_ui_mockup()
