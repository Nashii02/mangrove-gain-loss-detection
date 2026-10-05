"""
Generate formal PDF version of the Software Engineering Defense Document
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def generate_pdf():
    pdf_path = "Documentation/Software_Engineering_Defense_Document.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#143526'),
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2D6A4F'),
        alignment=TA_CENTER
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#143526'),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2D6A4F'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=14,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#143526')
    )

    story = []

    # Title Block
    story.append(Paragraph("Software Engineering 2 — Final Defense Specification", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Deep Learning-Based Detection of Mangrove Gain and Loss in Barangay Dulao, Aringay, La Union Using U-Net and Sentinel-2 Imagery", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Researchers:</b> Nash Francis M. Caluza, Reymark O. Boado, Elaiza Praise Y. Milana, Lyka B. Vejano<br/><b>Adviser:</b> Dr. Fernan H. Mendoza &nbsp;|&nbsp; <b>Institution:</b> DMMMSU-SLUC College of Computer Science &nbsp;|&nbsp; <b>Partner:</b> Aringay MENRO", meta_style))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2D6A4F'), spaceAfter=14))

    # SECTION 1: PROJECT OVERVIEW
    story.append(Paragraph("1. Project Overview", h1_style))
    story.append(Paragraph("<b>1.1 Ecological Context & Motivation:</b> Mangrove forests in Barangay Dulao, Aringay, La Union form an essential coastal barrier buffering the municipality against monsoonal typhoons, tidal scouring, and coastal erosion along Lingayen Gulf. Furthermore, they serve as high-capacity carbon sinks and vital estuarine breeding grounds for local artisanal fisheries. However, the ecosystem faces chronic pressures from aquaculture fishpond conversions, coastal residential encroachment, and storm surge damage.", body_style))
    story.append(Paragraph("<b>1.2 Problem Statement & Local Research Gap:</b> Monitoring the 316.74-hectare mangrove zone manually presents severe logistical and physical hazards due to soft intertidal mudflats and dense aerial prop roots. Conventional remote sensing relies on simple spectral index thresholding, which frequently misclassifies agricultural crops and fishpond algae as mangrove canopy. Furthermore, academic research rarely translates into accessible tools for local government units like Aringay MENRO, resulting in a usability barrier.", body_style))
    story.append(Paragraph("<b>1.3 General Objective:</b> To engineer an automated, web-based decision-support system that detects, classifies, and quantifies mangrove canopy gain and loss across Barangay Dulao from 2019 to 2024 by integrating Sentinel-2 Level-2A multi-spectral satellite imagery, a 5-channel modified U-Net deep learning model, and an interactive Flask/Leaflet web GIS prototype.", body_style))
    story.append(Paragraph("<b>1.4 Specific Objectives:</b>", h2_style))
    story.append(Paragraph("• <b>Specific Objective 1 (Data Engineering):</b> Ingest Copernicus Sentinel-2 MSI Level-2A surface reflectance (2019–2024 dry season); extract Green (B3), Red (B4), NIR (B8), and SWIR (B11); bilinearly resample Band 11 from 20m to 10m; compute normalized NDVI; and construct standardized 5-channel 256×256 input tensors.", bullet_style))
    story.append(Paragraph("• <b>Specific Objective 2 (AI Model Development):</b> Construct a 5-channel U-Net semantic segmentation network; optimize using an 80/20 train-validation partition, Adam optimizer (lr=0.001), Binary Cross-Entropy loss, and EarlyStopping; and evaluate via F1-score, IoU, and mAP across a 0.05–0.95 threshold sweep.", bullet_style))
    story.append(Paragraph("• <b>Specific Objective 3 (Post-Classification & Prototype):</b> Implement a Post-Classification Comparison (PCC) transition matrix algorithm mapping Gain, Loss, Stable Mangrove, and Stable Non-mangrove across all 15 pairwise annual epochs; develop a responsive three-tier web application using Flask, Leaflet.js, and Chart.js; and integrate automated one-click A4 PDF report generation for Aringay MENRO.", bullet_style))

    # SECTION 2: PROJECT SCOPE
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Project Scope & Delimitations", h1_style))
    story.append(Paragraph("<b>2.1 Geographic Delimitation:</b> The study is strictly delimited to the coastal mangrove zone of Barangay Dulao, Municipality of Aringay, Province of La Union, Philippines. The authoritative Region of Interest (ROI) is defined by a 25-vertex polygon spanning <b>exactly 316.74 hectares</b> (Bounding Box: 120.320°E to 120.343°E, 16.364°N to 16.388°N).", body_style))
    story.append(Paragraph("<b>2.2 Temporal Baseline:</b> Covers six consecutive dry-season epochs: <b>2019, 2020, 2021, 2022, 2023, and 2024</b>. Satellite scenes are restricted to <b>February 1 to April 30</b> with scene cloud cover strictly filtered to &lt; 20% to avoid monsoonal cloud masking and seasonal tidal variations.", body_style))
    
    # In-Scope vs Out-of-Scope Table
    scope_data = [
        [Paragraph("<b>In-Scope System Deliverables</b>", callout_style), Paragraph("<b>Out-of-Scope & System Delimitations</b>", callout_style)],
        [Paragraph("• Sentinel-2 L2A surface reflectance ingestion.<br/>• B3, B4, B8, B11 & NDVI 5-channel tensor generation.<br/>• Binary semantic segmentation via 5-channel U-Net.<br/>• Post-Classification Comparison for all 15 year pairs.<br/>• Interactive Leaflet map with Gain/Loss/ROI overlays.<br/>• Automated A4 PDF report generation for Aringay MENRO.", body_style),
         Paragraph("• Live on-the-fly orbital satellite data downloading.<br/>• Species-level taxonomic distinction (requires drone LiDAR).<br/>• Rainy season monitoring (cloud cover &gt; 70-80%).<br/>• Commercial high-cost satellite sensors (Maxar, Planet).<br/>• Autonomous drone field survey integration.", body_style)]
    ]
    t_scope = Table(scope_data, colWidths=[250, 250])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#E8F5E9')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#FFEBEE')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_scope)

    # SECTION 3: SOFTWARE DEVT METHODOLOGY
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Software Development Methodology", h1_style))
    story.append(Paragraph("<b>3.1 Process Model (Iterative & Incremental Development):</b> The project adopted the IID model (Thesis Manuscript, p. 11), advancing across eight sequential phases: (1) Domain Analysis & MENRO Consultation, (2) Satellite Scene Acquisition, (3) Preprocessing & Resampling, (4) Patch Preparation & 80/20 Partitioning, (5) U-Net Network Construction, (6) Training & EarlyStopping, (7) PCC Matrix Transition Engine, and (8) Web GIS Prototype & ReportLab PDF Integration.", body_style))
    story.append(Paragraph("<b>3.2 Data Partitioning Protocol:</b> The research team adopted an <b>80% Training / 20% Holdout Validation</b> split as the study-specific experimental protocol. The 80% partition is used by the Adam optimizer (lr=0.001) with Binary Cross-Entropy loss. The 20% holdout set monitors generalization and triggers EarlyStopping (patience=10 epochs). <i>Academic Integrity Rule: The 80/20 partition is an established experimental choice by the research team and is not attributed to external authors.</i>", body_style))
    story.append(Paragraph("<b>3.3 Quality Assurance & Verification:</b> Automated regression assertions verify that for every pairwise comparison: Area(ROI) = Area(Gain) + Area(Loss) + Area(Stable Mangrove) + Area(Stable Non-Mangrove) = 316.74 ha exactly.", body_style))

    # SECTION 4: SOFTWARE REQUIREMENTS & SYSTEM MODELS
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Software Requirements and System Models", h1_style))
    story.append(Paragraph("<b>4.1 Functional & Non-Functional Specifications:</b> The prototype satisfies five primary functional requirements (FR-01: Spatial Data Loader; FR-02: Pairwise Change Analyzer; FR-03: Cartographic Web Visualizer; FR-04: Extent Trend Calculator; FR-05: Automated PDF Generator) and critical non-functional constraints including sub-2-second API response times and 100% mathematical area conservation.", body_style))
    story.append(Paragraph("<b>4.2 Three-Tier Software Architecture:</b>", h2_style))
    story.append(Paragraph("• <b>Tier 1 (Presentation):</b> Responsive HTML5/CSS3 client, Leaflet.js interactive cartography, and Chart.js historical trend rendering.<br/>• <b>Tier 2 (Application Backend):</b> Python Flask WSGI server hosting REST endpoints (/api/study-area, /api/statistics, /api/change-detection) and headless ReportLab PDF generator.<br/>• <b>Tier 3 (Data & Models):</b> Pre-processed Sentinel-2 L2A rasters, 25-point ROI GeoJSON (316.74 ha), and U-Net classification artifacts.", body_style))
    story.append(Paragraph("<b>4.3 Multi-Spectral Tensor & Mathematical Models:</b>", h2_style))
    story.append(Paragraph("• <b>5D Input Tensor:</b> 256×256×5 array [B3 (Green 560nm), B4 (Red 665nm), B8 (NIR 842nm), B11 (SWIR 1610nm resampled to 10m), NDVI normalized to [0, 1]].<br/>• <b>NDVI Formula:</b> NDVI = (B8 - B4) / (B8 + B4).<br/>• <b>U-Net Model:</b> 4-level encoder-decoder with skip connections and Sigmoid probability output.<br/>• <b>PCC Matrix:</b> Categorizes pixels into Gain (+1), Loss (-1), Stable Mangrove (2), and Stable Non-mangrove (0). Pixel count multiplied by 0.01 yields exact hectarage.", body_style))

    # SECTION 5: SOFTWARE DEMO
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Software Demo & Operational Walkthrough", h1_style))
    story.append(Paragraph("The software prototype is fully operational and demonstrated through a four-step municipal workflow:", body_style))
    story.append(Paragraph("• <b>Step 1 (System Initialization):</b> Launch server via `python app.py` and open `http://127.0.0.1:5000/`. Observe the Leaflet map automatically centered on Barangay Dulao with the yellow 25-point ROI boundary line.", bullet_style))
    story.append(Paragraph("• <b>Step 2 (Select Baseline & Target):</b> Using the sidebar controls, select Baseline Year T₁ (e.g., 2019) and Comparison Year T₂ (e.g., 2024), then click 'Analyze Change'.", bullet_style))
    story.append(Paragraph("• <b>Step 3 (Cartographic & Metric Inspection):</b> Inspect the instantaneous update of net gain (+ ha), net loss (- ha), interactive green gain and red loss vector layers, and the multi-temporal trend chart.", bullet_style))
    story.append(Paragraph("• <b>Step 4 (Automated Report Export):</b> Click 'Export MENRO PDF Report' to generate and download a formal, printable A4 conservation report.", bullet_style))
    story.append(Paragraph("<i>Demonstration Transparency: The running system demonstrates complete functional execution using controlled demonstration benchmark values to validate the workflow prior to final ground-truth mask sign-off by Aringay MENRO.</i>", meta_style))

    # SECTION 6: STATUS & DEFENSE Q&A
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Implementation Status & Defense Preparation", h1_style))
    status_data = [
        [Paragraph("<b>Component</b>", callout_style), Paragraph("<b>Status</b>", callout_style), Paragraph("<b>Implementation Remarks</b>", callout_style)],
        [Paragraph("Web Frontend & Cartography", body_style), Paragraph("<font color='#166534'><b>IMPLEMENTED</b></font>", body_style), Paragraph("Interactive Leaflet map, layer controls, and Chart.js charts.", body_style)],
        [Paragraph("Flask Backend & REST API", body_style), Paragraph("<font color='#166534'><b>IMPLEMENTED</b></font>", body_style), Paragraph("WSGI server, JSON contracts, and error handlers tested.", body_style)],
        [Paragraph("Automated PDF Engine", body_style), Paragraph("<font color='#166534'><b>IMPLEMENTED</b></font>", body_style), Paragraph("ReportLab engine builds formatted A4 reports dynamically.", body_style)],
        [Paragraph("Sentinel-2 Preprocessing", body_style), Paragraph("<font color='#166534'><b>IMPLEMENTED</b></font>", body_style), Paragraph("B3, B4, B8, B11 resampling, and NDVI 5D tensor pipeline.", body_style)],
        [Paragraph("5-Channel U-Net Architecture", body_style), Paragraph("<font color='#166534'><b>IMPLEMENTED</b></font>", body_style), Paragraph("Encoder-decoder with skip connections and sweep scripts.", body_style)],
        [Paragraph("Independent Mask Validation", body_style), Paragraph("<font color='#B45309'><b>PENDING</b></font>", body_style), Paragraph("Undergoing independent ground-truth sign-off by Aringay MENRO.", body_style)],
        [Paragraph("Final Weights & Metrics", body_style), Paragraph("<font color='#B45309'><b>PENDING</b></font>", body_style), Paragraph("GPU training on Colab will follow immediately after MENRO validation.", body_style)],
        [Paragraph("Live Satellite Ingestion", body_style), Paragraph("<font color='#64748B'><b>OUT OF SCOPE</b></font>", body_style), Paragraph("Decision support tool operating on pre-processed composites.", body_style)]
    ]
    t_stat = Table(status_data, colWidths=[160, 100, 240])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stat)

    doc.build(story)
    print(f"Generated defense document PDF: {pdf_path}")

if __name__ == '__main__':
    generate_pdf()
