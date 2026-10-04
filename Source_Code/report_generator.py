"""
Report Generator for Aringay MENRO
Mangrove Monitoring System — Brgy. Dulao, Aringay, La Union
Generates a formal multi-page PDF report with methodology, statistics table,
map visualization, disclaimer, and official MENRO signature lines.
"""

import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group

NAVY = colors.HexColor("#1A5276")
FOREST = colors.HexColor("#1B4332")
GREEN = colors.HexColor("#2ECC71")
RED = colors.HexColor("#E74C3C")
LIGHT_BG = colors.HexColor("#F8F9FA")
BORDER_COLOR = colors.HexColor("#D5DBDB")

def build_pdf_report(demo_area_ha, years, study_area, get_change_fn=None):
    """
    Builds a formal PDF report in memory and returns BytesIO buffer.
    Ensures strictly NO prohibited technical terms ('segmentation', 'IoU',
    'inference', 'GeoTIFF', 'threshold', 'U-Net') appear in user-facing text.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        alignment=1, # Center
    )
    sub_title_style = ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.dimgray,
        alignment=1,
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=NAVY,
        spaceAfter=6,
        spaceBefore=10,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.black,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.dimgray,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
    )

    story = []

    # 1. Official Header
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", sub_title_style))
    story.append(Paragraph("PROVINCE OF LA UNION · MUNICIPALITY OF ARINGAY", sub_title_style))
    story.append(Paragraph("MUNICIPAL ENVIRONMENT AND NATURAL RESOURCES OFFICE (MENRO)", ParagraphStyle(
        "MenroHeader", parent=sub_title_style, fontName="Helvetica-Bold", fontSize=10, textColor=FOREST
    )))
    story.append(Spacer(1, 8))
    story.append(Paragraph("MANGROVE COVER MONITORING &amp; CHANGE DETECTION REPORT", title_style))
    story.append(Paragraph(f"Study Area: {study_area['name']} · Observation Period: 2019–2024", sub_title_style))
    story.append(Spacer(1, 12))

    # Divider line
    d_line = Drawing(520, 2)
    d_line.add(Line(0, 1, 520, 1, strokeColor=NAVY, strokeWidth=1.5))
    story.append(d_line)
    story.append(Spacer(1, 10))

    # 2. Executive Summary
    story.append(Paragraph("1. Executive Summary", section_heading))
    start_yr, end_yr = years[0], years[-1]
    start_area = demo_area_ha[start_yr]
    end_area = demo_area_ha[end_yr]
    net_total = round(end_area - start_area, 2)
    net_status = "growth" if net_total >= 0 else "reduction"
    equiv_fields = round(abs(net_total) * 1.4, 1)

    summary_text = (
        f"This official monitoring report details mapped mangrove forest extent and vegetative changes "
        f"along the coastal intertidal zone of Barangay Dulao, Aringay, La Union from {start_yr} to {end_yr}. "
        f"In {start_yr}, mapped mangrove vegetation covered <b>{start_area:.2f} hectares</b>. "
        f"By {end_yr}, mapped mangrove cover measured <b>{end_area:.2f} hectares</b>, indicating a net {net_status} "
        f"of <b>{abs(net_total):.2f} hectares</b> (equivalent to about {equiv_fields} standard football fields). "
        f"These findings assist the Aringay MENRO in prioritizing coastal rehabilitation, evaluating conservation "
        f"success, and targeting shoreline patrols."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))

    # 3. Methodology Summary (Plain Language, strictly no prohibited terms)
    story.append(Paragraph("2. Methodology Overview", section_heading))
    method_text = (
        "<b>Data Source:</b> Observations were acquired from European Space Agency Sentinel-2 satellite imagery "
        "captured at the same seasonal period each year to minimize tidal and weather variability.<br/>"
        "<b>Spatial Resolution:</b> The computer model scans satellite photos on a 10-meter grid, where each individual "
        "scan block corresponds to 100 square meters (0.01 hectare, or about the size of a tennis court).<br/>"
        "<b>Vegetation Analysis:</b> Our computer vision model studied spectral reflectance patterns and vegetation greenness "
        "to distinguish mangrove canopies from open coastal water, tidal flats, and terrestrial vegetation.<br/>"
        "<b>Change Classification:</b> Consecutive observation years are compared across four standard categories:<br/>"
        "&nbsp;&nbsp;• <b>Stable Mangrove:</b> Forest canopy that remained present and healthy across both survey years.<br/>"
        "&nbsp;&nbsp;• <b>Mapped Gain:</b> Newly grown or regenerated mangroves appearing in previously unvegetated shoreline.<br/>"
        "&nbsp;&nbsp;• <b>Mapped Loss:</b> Mangroves that disappeared or were removed since the prior survey year.<br/>"
        "&nbsp;&nbsp;• <b>Stable Non-mangrove:</b> Surrounding open water, tidal mudflats, and shoreline that remained non-mangrove across both years."
    )
    story.append(Paragraph(method_text, body_style))
    story.append(Spacer(1, 10))

    # 4. Statistics Table
    story.append(Paragraph("3. Annual Cover &amp; Transition Statistics", section_heading))
    table_data = [
        [
            Paragraph("<b>Period / Year</b>", table_cell_bold),
            Paragraph("<b>Mapped Cover</b>", table_cell_bold),
            Paragraph("<b>Mapped Gain</b>", table_cell_bold),
            Paragraph("<b>Mapped Loss</b>", table_cell_bold),
            Paragraph("<b>Net Change</b>", table_cell_bold),
            Paragraph("<b>What This Means</b>", table_cell_bold),
        ]
    ]

    for i in range(len(years) - 1):
        y1 = years[i]
        y2 = years[i + 1]
        a1 = demo_area_ha[y1]
        a2 = demo_area_ha[y2]
        if get_change_fn:
            ch = get_change_fn(y1, y2)
            gain = ch["gain_ha"]
            loss = ch["loss_ha"]
            net = ch["net_ha"]
        else:
            gain = max(0.0, a2 - a1)
            loss = max(0.0, a1 - a2)
            net = round(a2 - a1, 2)
        sign = "+" if net >= 0 else "−"
        meaning = "Forest expansion" if net > 0 else "Forest loss" if net < 0 else "Stable cover"

        table_data.append([
            Paragraph(f"{y1} → {y2}", table_cell),
            Paragraph(f"{a2:.2f} ha", table_cell),
            Paragraph(f"+{gain:.2f} ha", table_cell),
            Paragraph(f"−{loss:.2f} ha", table_cell),
            Paragraph(f"{sign}{abs(net):.2f} ha", table_cell_bold),
            Paragraph(f"{meaning} ({round(abs(net)*1.4, 1)} fields)", table_cell),
        ])

    stats_table = Table(table_data, colWidths=[65, 65, 65, 65, 65, 175])
    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("ALIGN", (1, 0), (4, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 12))

    # 5. Study Area & Visual Map
    story.append(Paragraph("4. Coastal Study Area &amp; Change Map Reference", section_heading))
    map_intro = (
        f"<b>Location Coordinates:</b> Barangay Dulao Coastline [120.355°E–120.375°E, 16.305°N–16.325°N].<br/>"
        f"The visual representation below reflects mapped mangrove distribution and localized transitions:"
    )
    story.append(Paragraph(map_intro, body_style))
    story.append(Spacer(1, 6))

    # Clean Drawing for Map & Legend
    map_draw = Drawing(520, 115)
    # Background card
    map_draw.add(Rect(0, 0, 520, 115, fillColor=LIGHT_BG, strokeColor=BORDER_COLOR, strokeWidth=0.5, rx=4, ry=4))
    # Simulated coastal coastline block
    map_draw.add(Rect(20, 15, 140, 85, fillColor=colors.HexColor("#EAECEE"), strokeColor=colors.HexColor("#BDC3C7"), strokeWidth=1))
    map_draw.add(String(25, 88, "Shoreline / Water Zone", fontSize=7, fontName="Helvetica", fillColor=colors.dimgray))
    # Mangrove patches
    map_draw.add(Rect(50, 42, 45, 30, fillColor=FOREST, strokeColor=colors.black, strokeWidth=0.5))
    map_draw.add(Rect(98, 48, 22, 18, fillColor=GREEN, strokeColor=FOREST, strokeWidth=1))
    map_draw.add(Rect(75, 30, 18, 12, fillColor=RED, strokeColor=colors.HexColor("#780016"), strokeWidth=1))

    # Legend text & swatches
    map_draw.add(String(180, 96, "MAP CLASSIFICATION LEGEND:", fontSize=8.5, fontName="Helvetica-Bold", fillColor=NAVY))

    # Stable Mangrove
    map_draw.add(Rect(180, 74, 14, 11, fillColor=FOREST, strokeColor=colors.black, strokeWidth=0.5))
    map_draw.add(String(200, 76, "● Stable Mangrove — Present in both comparison years", fontSize=7.5, fontName="Helvetica", fillColor=colors.black))

    # Mapped Gain
    map_draw.add(Rect(180, 55, 14, 11, fillColor=GREEN, strokeColor=FOREST, strokeWidth=1))
    map_draw.add(String(200, 57, "▲ Mapped Gain — Newly grown or appeared mangrove stands", fontSize=7.5, fontName="Helvetica", fillColor=colors.black))

    # Mapped Loss
    map_draw.add(Rect(180, 36, 14, 11, fillColor=RED, strokeColor=colors.HexColor("#780016"), strokeWidth=1))
    map_draw.add(String(200, 38, "▼ Mapped Loss — Disappeared or removed mangrove areas (Priority for patrol)", fontSize=7.5, fontName="Helvetica", fillColor=colors.black))

    # Stable Non-mangrove
    map_draw.add(Rect(180, 17, 14, 11, fillColor=colors.HexColor("#dee2e6"), strokeColor=colors.HexColor("#adb5bd"), strokeWidth=1))
    map_draw.add(String(200, 19, "◻ Stable Non-mangrove — Open water, mudflats, and non-mangrove coastline", fontSize=7.5, fontName="Helvetica", fillColor=colors.black))

    story.append(map_draw)
    story.append(Spacer(1, 14))

    # 6. Official Disclaimer
    story.append(Paragraph("5. Advisory &amp; Disclaimer", section_heading))
    disclaimer_text = (
        "<b>OFFICIAL ADVISORY:</b> All statistical summaries, transition figures, and visual maps in this document "
        "are computer-mapped estimates derived from 10-meter Sentinel-2 satellite imagery. This document is intended "
        "to assist the Aringay Municipal Environment and Natural Resources Office (MENRO) in coastal management, "
        "monitoring, and priority area assessment. Field ground-truthing and on-site inspection are strongly "
        "recommended before formal regulatory action or replanting investment."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    story.append(Spacer(1, 18))

    # 7. Signature Area
    sig_block = [
        [
            Paragraph("<b>Prepared by:</b>", table_cell),
            Paragraph("<b>Reviewed &amp; Certified by:</b>", table_cell),
        ],
        [
            Spacer(1, 28),
            Spacer(1, 28),
        ],
        [
            Paragraph("____________________________________________<br/><b>GIS &amp; Monitoring Analyst</b><br/>Mangrove Gain &amp; Loss Detection System", table_cell),
            Paragraph("____________________________________________<br/><b>Municipal Environment &amp; Natural Resources Officer</b><br/>Aringay MENRO · Municipality of Aringay, La Union", table_cell),
        ],
        [
            Paragraph("Date: ________________________", table_cell),
            Paragraph("Date: ________________________", table_cell),
        ]
    ]
    sig_table = Table(sig_block, colWidths=[250, 260])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(KeepTogether(sig_table))

    # Build the document
    doc.build(story)
    buf.seek(0)
    return buf
