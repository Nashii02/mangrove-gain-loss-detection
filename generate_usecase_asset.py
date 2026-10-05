import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_usecase_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, "Use Case & System Boundary Model", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#143526')
    ax.text(0.5, 0.88, "Mangrove Gain & Loss Monitoring System — Functional Interaction", 
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#475569')

    # System Boundary Box
    sys_box = patches.FancyBboxPatch((0.26, 0.08), 0.48, 0.74,
                                     boxstyle="round,pad=0.02,rounding_size=0.03",
                                     facecolor="#F8FAFC", edgecolor="#2D6A4F", linewidth=2.5, linestyle='--')
    ax.add_patch(sys_box)
    ax.text(0.50, 0.78, "System Boundary: Mangrove Monitoring Platform",
            ha='center', va='center', fontsize=10, fontweight='bold', color='#2D6A4F')

    # Actor 1: Aringay MENRO Officer (Left)
    ax.text(0.12, 0.62, "👤", ha='center', va='center', fontsize=28)
    ax.text(0.12, 0.52, "Aringay MENRO\nOfficer\n(Primary User)", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#0F172A')

    # Actor 2: GIS / Remote Sensing Researcher (Right)
    ax.text(0.88, 0.62, "🧑‍🔬", ha='center', va='center', fontsize=28)
    ax.text(0.88, 0.52, "GIS / ML\nResearcher\n(Administrator)", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#0F172A')

    # Use Cases (Ovals in center)
    usecases = [
        {"y": 0.68, "text": "UC-1: Select Temporal Baseline (T₁ vs T₂)"},
        {"y": 0.54, "text": "UC-2: Execute Post-Classification Change Analysis"},
        {"y": 0.40, "text": "UC-3: Inspect Interactive Cartographic Layers"},
        {"y": 0.26, "text": "UC-4: Analyze Multi-Temporal Extent Statistics"},
        {"y": 0.13, "text": "UC-5: Generate Formal A4 PDF Report"}
    ]

    for uc in usecases:
        ellipse = patches.FancyBboxPatch((0.30, uc["y"] - 0.04), 0.40, 0.08,
                                         boxstyle="round,pad=0.01,rounding_size=0.04",
                                         facecolor="#FFFFFF", edgecolor="#143526", linewidth=1.5)
        ax.add_patch(ellipse)
        ax.text(0.50, uc["y"], uc["text"], ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#0F172A')

        # Connect to Actor 1 (MENRO Officer)
        ax.plot([0.18, 0.30], [0.55, uc["y"]], color='#2D6A4F', lw=1.2, linestyle='-')
        # Connect to Actor 2 (Researcher) for core analytics
        if uc["y"] >= 0.26:
            ax.plot([0.70, 0.82], [uc["y"], 0.55], color='#0284C7', lw=1.2, linestyle='-')

    plt.tight_layout()
    plt.savefig('extracted_assets/requirements_usecase_model.png', dpi=300)
    plt.close()
    print("Generated extracted_assets/requirements_usecase_model.png")

if __name__ == '__main__':
    generate_usecase_diagram()
