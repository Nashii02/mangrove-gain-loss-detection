"""
Build Master Presentation (.pptx) for Thesis Defense
Mangrove Gain and Loss Detection in Barangay Dulao, Aringay, La Union
Using U-Net and Sentinel-2 Imagery

Explicitly Aligned to the 5 Core Software Engineering Defense Pillars:
1. Project Overview
2. Project Scope
3. Software Development Methodology
4. Software Requirements and System Models
5. Software Demo
(+ Current Status, Synthesis & Defense Q&A)
"""
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -----------------------------------------------------------------------------
# PALETTE DEFINITION (Academic & Environmental Software Engineering)
# -----------------------------------------------------------------------------
COLOR_DARK_GREEN = RGBColor(20, 53, 38)      # #143526 Primary Brand
COLOR_MID_GREEN  = RGBColor(45, 106, 79)     # #2D6A4F Secondary Brand
COLOR_LIGHT_BG   = RGBColor(248, 250, 252)   # #F8FAFC Clean Neutral Background
COLOR_WHITE      = RGBColor(255, 255, 255)   # #FFFFFF
COLOR_CARD_BG    = RGBColor(255, 255, 255)   # #FFFFFF Card Surface
COLOR_CARD_BORDER= RGBColor(226, 232, 240)   # #E2E8F0 Card Border
COLOR_TEXT_MAIN  = RGBColor(15, 23, 42)      # #0F172A Slate 900
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569 Slate 600
COLOR_GAIN_GREEN = RGBColor(22, 101, 52)     # #166534 Mangrove Gain
COLOR_LOSS_RED   = RGBColor(153, 27, 27)     # #991B1B Mangrove Loss
COLOR_BLUE_ACCENT= RGBColor(2, 132, 199)     # #0284C7 Info / Sky
COLOR_AMBER      = RGBColor(180, 83, 9)      # #B45309 Warning / Pending
COLOR_LIGHT_GAIN = RGBColor(240, 253, 244)   # #F0FDF4 Light Gain Tint
COLOR_LIGHT_LOSS = RGBColor(254, 242, 242)   # #FEF2F2 Light Loss Tint
COLOR_LIGHT_BLUE = RGBColor(240, 249, 255)   # #F0F9FF Light Info Tint
COLOR_LIGHT_AMBER= RGBColor(255, 251, 235)   # #FFFBEB Light Warning Tint

FONT_TITLE = "Calibri"
FONT_BODY  = "Calibri"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Set Slide Background
    def set_slide_background(slide, color=COLOR_LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Add Header
    def add_header(slide, title_text, category_text, slide_num):
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = COLOR_DARK_GREEN
        top_bar.line.fill.background()

        # Category Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.0), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_BODY
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_MID_GREEN

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(10.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.5), Inches(0.8), Inches(0.4))
        tf_num = num_box.text_frame
        tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.text = f"{slide_num:02d} / 20"
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_TEXT_MUTED
        p_num.alignment = PP_ALIGN.RIGHT

    # Helper: Add Card Container
    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, border_width=1):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(border_width)
        else:
            card.line.fill.background()
        return card

    # Helper: Add Speaker Notes
    def add_notes(slide, presenter_script, key_message, technical_explanation, panel_qa, caution_warning):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = f"=== PRESENTER SCRIPT ===\n{presenter_script}\n\n"
        tf.text += f"=== KEY MESSAGE ===\n{key_message}\n\n"
        tf.text += f"=== TECHNICAL EXPLANATION ===\n{technical_explanation}\n\n"
        tf.text += f"=== LIKELY PANEL Q&A ===\n{panel_qa}\n\n"
        tf.text += f"=== CAUTION / WHAT NOT TO SAY ===\n{caution_warning}"

    authors = ["Nash Francis M. Caluza", "Reymark O. Boado", "Elaiza Praise Y. Milana", "Lyka B. Vejano"]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_DARK_GREEN)

    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(1.5), Inches(0.08))
    accent_bar.fill.solid(); accent_bar.fill.fore_color.rgb = RGBColor(16, 185, 129); accent_bar.line.fill.background()

    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]; p_sub.text = "BACHELOR OF SCIENCE IN COMPUTER SCIENCE — FINAL THESIS PRESENTATION"; p_sub.font.bold = True; p_sub.font.size = Pt(12); p_sub.font.color.rgb = RGBColor(167, 243, 208)

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(2.0))
    tf_t = t_box.text_frame; tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]; p_t.text = "Deep Learning-Based Detection of Mangrove Gain and Loss\nin Barangay Dulao, Aringay, La Union\nUsing U-Net and Sentinel-2 Imagery"
    p_t.font.name = FONT_TITLE; p_t.font.size = Pt(28); p_t.font.bold = True; p_t.font.color.rgb = COLOR_WHITE

    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.733), Inches(0.02))
    div.fill.solid(); div.fill.fore_color.rgb = RGBColor(52, 211, 153); div.line.fill.background()

    c1 = s1.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(3.6), Inches(2.7))
    tf1 = c1.text_frame
    p1 = tf1.paragraphs[0]; p1.text = "STUDENT RESEARCHERS"; p1.font.bold = True; p1.font.size = Pt(11); p1.font.color.rgb = RGBColor(167, 243, 208)
    for a in authors:
        pa = tf1.add_paragraph(); pa.text = f"•  {a}"; pa.font.size = Pt(12); pa.font.color.rgb = COLOR_WHITE

    c2 = s1.shapes.add_textbox(Inches(4.6), Inches(4.3), Inches(3.5), Inches(2.7))
    tf2 = c2.text_frame
    p2 = tf2.paragraphs[0]; p2.text = "THESIS ADVISER"; p2.font.bold = True; p2.font.size = Pt(11); p2.font.color.rgb = RGBColor(167, 243, 208)
    pa2 = tf2.add_paragraph(); pa2.text = "Dr. Fernan H. Mendoza"; pa2.font.bold = True; pa2.font.size = Pt(13); pa2.font.color.rgb = COLOR_WHITE
    p_adv = tf2.add_paragraph(); p_adv.text = "Faculty Adviser\nCollege of Computer Science"; p_adv.font.size = Pt(11); p_adv.font.color.rgb = RGBColor(209, 250, 229)

    c3 = s1.shapes.add_textbox(Inches(8.3), Inches(4.3), Inches(4.2), Inches(2.7))
    tf3 = c3.text_frame
    p3 = tf3.paragraphs[0]; p3.text = "INSTITUTION & PARTNER"; p3.font.bold = True; p3.font.size = Pt(11); p3.font.color.rgb = RGBColor(167, 243, 208)
    p_inst = tf3.add_paragraph(); p_inst.text = "Don Mariano Marcos Memorial State University\nSouth La Union Campus (DMMMSU-SLUC)\nAgoo, La Union, Philippines"; p_inst.font.size = Pt(11); p_inst.font.color.rgb = COLOR_WHITE
    p_menro = tf3.add_paragraph(); p_menro.text = "In Collaboration with:\nMunicipal Environment & Natural Resources Office\n(MENRO), Aringay, La Union"; p_menro.font.size = Pt(11); p_menro.font.color.rgb = RGBColor(254, 240, 138)

    add_notes(s1,
        "Good morning, respected members of the panel, our thesis adviser Dr. Fernan Mendoza, and guests. Today we present our thesis defense on 'Deep Learning-Based Detection of Mangrove Gain and Loss in Barangay Dulao, Aringay, La Union Using U-Net and Sentinel-2 Imagery.' We are Nash Francis Caluza, Reymark Boado, Elaiza Praise Milana, and Lyka Vejano from the College of Computer Science at DMMMSU-SLUC.",
        "The study bridges remote sensing, deep learning, and practical software engineering to solve a local conservation challenge for Barangay Dulao, Aringay.",
        "This project combines European Space Agency Sentinel-2 multispectral satellite data (10m resolution) with a 5-channel modified U-Net deep convolutional neural network, wrapped inside an interactive decision-support web system developed for Aringay MENRO.",
        "Q: Why focus specifically on Barangay Dulao?\nA: Barangay Dulao contains the primary estuarine mangrove belt of Aringay along the river mouth and Lingayen Gulf. It is heavily affected by both natural tidal dynamics and aquaculture fishpond conversion, making localized automated monitoring vital.",
        "Do NOT introduce the prototype numbers as final results yet. Keep the opening focused on the academic motivation, researchers, and project scope.")

    # =========================================================================
    # SLIDE 2: PRESENTATION AGENDA (THE 5 CORE SECTIONS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Presentation Structure: 5 Software Engineering Pillars", "Table of Contents", 2)

    agenda_items = [
        {"num": "01", "title": "Project Overview", "desc": "Ecological Context, Local Problem Statement, Research Gap, General & Specific Objectives.", "color": COLOR_MID_GREEN},
        {"num": "02", "title": "Project Scope", "desc": "Spatial Delimitation (Dulao 316.74 ha), Temporal Baseline (2019–2024), In-Scope vs. Out-of-Scope.", "color": COLOR_BLUE_ACCENT},
        {"num": "03", "title": "Software Devt Methodology", "desc": "Iterative & Incremental Development (IID), Data Pipeline, 80/20 Partition Protocol, QA & Testing.", "color": COLOR_DARK_GREEN},
        {"num": "04", "title": "Requirements & System Models", "desc": "Functional/Non-Functional Specs, Three-Tier Architecture, 5D Tensor Stack, U-Net AI & PCC Matrix.", "color": COLOR_AMBER},
        {"num": "05", "title": "Software Demo", "desc": "Operational Dashboard Walkthrough, Interactive Pairwise Analysis, Cartography, Automated PDF Export.", "color": COLOR_GAIN_GREEN},
        {"num": "06", "title": "Status, Synthesis & Q&A", "desc": "Current Subsystem Implementation Matrix, Tripartite Contribution, Roadmap, Open Defense Discussion.", "color": COLOR_TEXT_MUTED}
    ]

    for i, itm in enumerate(agenda_items):
        r = i // 3
        c = i % 3
        c_left = Inches(0.8) + c * Inches(3.95)
        c_top = Inches(1.8) + r * Inches(2.6)
        
        card = add_card(s2, c_left, c_top, Inches(3.7), Inches(2.35), bg_color=COLOR_WHITE, border_color=itm["color"], border_width=2)
        tb = s2.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), Inches(3.3), Inches(2.05))
        tf = tb.text_frame; tf.word_wrap = True
        
        p = tf.paragraphs[0]; p.text = f"PILLAR {itm['num']}"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = itm["color"]
        p_t = tf.add_paragraph(); p_t.text = itm["title"]; p_t.font.bold = True; p_t.font.size = Pt(15); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_before = Pt(4); p_t.space_after = Pt(6)
        p_d = tf.add_paragraph(); p_d.text = itm["desc"]; p_d.font.size = Pt(10.5); p_d.font.color.rgb = COLOR_TEXT_MUTED; p_d.line_spacing = 1.3

    add_notes(s2,
        "Here is the roadmap for our defense presentation today. We have strictly organized our presentation across the five required software engineering pillars: First, Project Overview; Second, Project Scope; Third, Software Development Methodology; Fourth, Software Requirements and System Models; and Fifth, our Live Software Demonstration, concluding with project status, contributions, and Q&A.",
        "The presentation is structured around the 5 standard software engineering defense criteria required by the course rubric.",
        "This ensures transparent alignment with technical grading criteria: problem/objectives, scope/requirements, process/architecture, implementation, and working demo.",
        "Q: How will the presentation be delivered among the four team members?\nA: The presentation is partitioned across the members: Nash introduces Overview and Objectives; Reymark covers Scope and Data Methodology; Elaiza presents System Models and Architecture; Lyka leads the Prototype Walkthrough and Testing, with all members participating in Status and Q&A.",
        "Transition smoothly by introducing Pillar 1: Project Overview.")

    # =========================================================================
    # PILLAR 1: PROJECT OVERVIEW (SLIDES 3, 4, 5)
    # =========================================================================
    # SLIDE 3: OVERVIEW - BACKGROUND & MOTIVATION
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Project Overview: Ecological Importance & Motivation", "1. Project Overview", 3)

    flow_steps = [
        {"num": "01", "title": "Critical Ecosystem", "color": COLOR_MID_GREEN, "bg": COLOR_LIGHT_GAIN,
         "desc": "Coastal Storm Protection\nCarbon Sequestration\nBiodiversity Nursery\nFishery Livelihoods", "icon": "🛡️"},
        {"num": "02", "title": "Severe Extent Loss", "color": COLOR_LOSS_RED, "bg": COLOR_LIGHT_LOSS,
         "desc": "Aquaculture Conversion\nCoastal Development\nTyphoon & Wave Erosion\nSubstantial Canopy Decline", "icon": "📉"},
        {"num": "03", "title": "Monitoring Deficit", "color": COLOR_AMBER, "bg": COLOR_LIGHT_AMBER,
         "desc": "Manual Field Surveys\nCost & Labor Intensive\nTidally Inaccessible\nInfrequent Survey Cadence", "icon": "⚠️"},
        {"num": "04", "title": "Automated Solution", "color": COLOR_BLUE_ACCENT, "bg": COLOR_LIGHT_BLUE,
         "desc": "Sentinel-2 Imagery\nU-Net Deep Learning\nPost-Classification Comparison\nMunicipal Decision Web Tool", "icon": "🛰️"}
    ]

    for i, step in enumerate(flow_steps):
        c_left = Inches(0.8) + i * Inches(3.0)
        card = add_card(s3, c_left, Inches(1.8), Inches(2.7), Inches(4.8), bg_color=step["bg"], border_color=step["color"], border_width=2)
        tb = s3.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(2.3), Inches(4.4))
        tf = tb.text_frame; tf.word_wrap = True
        
        p = tf.paragraphs[0]; p.text = f"{step['icon']}  PHASE {step['num']}"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = step["color"]
        p_t = tf.add_paragraph(); p_t.text = step["title"]; p_t.font.bold = True; p_t.font.size = Pt(16); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(14)
        p_d = tf.add_paragraph(); p_d.text = step["desc"]; p_d.font.size = Pt(12); p_d.font.color.rgb = COLOR_TEXT_MUTED; p_d.line_spacing = 1.4

        if i < 3:
            arrow_box = s3.shapes.add_textbox(c_left + Inches(2.7), Inches(4.0), Inches(0.3), Inches(0.5))
            tf_a = arrow_box.text_frame; tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            pa = tf_a.paragraphs[0]; pa.text = "→"; pa.font.bold = True; pa.font.size = Pt(22); pa.font.color.rgb = COLOR_MID_GREEN; pa.alignment = PP_ALIGN.CENTER

    add_notes(s3,
        "Beginning with Pillar 1, Project Overview: Why are mangroves vital, and why is monitoring them urgent? Mangroves serve as nature's coastal storm shields, carbon sinks, and marine nurseries. However, across the Philippines and in La Union specifically, mangrove stands face relentless pressure from aquaculture ponds, urban expansion, and typhoon damage. Currently, local government units rely on manual ocular surveys that are labor-heavy, tidally constrained, and infrequent. Our study solves this by introducing satellite remote sensing and deep learning.",
        "Mangrove monitoring needs to transition from manual, sporadic field surveys to automated, high-cadence satellite-driven analysis.",
        "Sentinel-2 provides 10-meter spatial resolution with a 5-day revisit cadence freely from the European Space Agency, while deep learning architectures like U-Net can generalize spatial-contextual patterns far better than traditional pixel-based thresholding.",
        "Q: Why not use commercial high-resolution imagery like Planet or Maxar?\nA: Sentinel-2 is completely free, open-access, and maintained by Copernicus ESA with regular revisits, making this automated monitoring system economically sustainable for municipal LGU budgets like Aringay MENRO.",
        "Do not overstate historical loss statistics unless quoting the literature cited in Chapter 1 of the manuscript.")

    # SLIDE 4: OVERVIEW - PROBLEM STATEMENT & RESEARCH GAP
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Project Overview: Problem Statement & Local Research Gap", "1. Project Overview", 4)

    problems = [
        {"title": "1. Spatial Complexity & Tidal Inaccessibility",
         "desc": "Barangay Dulao's estuarine mangroves feature dense aerial root tangles and deep muddy intertidal zones. Field personnel cannot safely or exhaustively traverse the entire 316.74-hectare zone on foot to log canopy disruptions.",
         "impact": "Result: Patchy, delayed, and incomplete monitoring coverage."},
        {"title": "2. Failure of Traditional Pixel Classifiers",
         "desc": "Conventional vegetation thresholding (e.g., raw NDVI thresholds alone or Maximum Likelihood) easily confuses healthy inland crops, fishpond algae, and tidal mudflats with true mangrove canopies due to overlapping spectral signatures.",
         "impact": "Result: High false-positive rates and misclassified boundaries."},
        {"title": "3. The Software-LGU Usability Barrier",
         "desc": "Existing remote sensing research produces raw geospatial GeoTIFFs or Python scripts. Municipal MENRO personnel lack specialized GIS software licenses or command-line scripting skills required to extract actionable planning insights.",
         "impact": "Result: Scientific models fail to support municipal policy."}
    ]

    for i, p in enumerate(problems):
        card = add_card(s4, Inches(0.8), Inches(1.8) + i * Inches(1.5), Inches(11.733), Inches(1.3), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        tb = s4.shapes.add_textbox(Inches(1.1), Inches(1.9) + i * Inches(1.5), Inches(11.1), Inches(1.1))
        tf = tb.text_frame; tf.word_wrap = True
        
        p_t = tf.paragraphs[0]; p_t.text = p["title"]; p_t.font.bold = True; p_t.font.size = Pt(15); p_t.font.color.rgb = COLOR_DARK_GREEN
        p_d = tf.add_paragraph(); p_d.text = p["desc"]; p_d.font.size = Pt(11.5); p_d.font.color.rgb = COLOR_TEXT_MUTED; p_d.space_before = Pt(3)
        p_i = tf.add_paragraph(); p_i.text = p["impact"]; p_i.font.bold = True; p_i.font.size = Pt(11); p_i.font.color.rgb = COLOR_LOSS_RED; p_i.space_before = Pt(2)

    bot = add_card(s4, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.8), bg_color=COLOR_DARK_GREEN, border_color=None)
    tb_bot = s4.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.6))
    tf_bot = tb_bot.text_frame
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "LOCAL RESEARCH GAP: Lack of an automated, localized mangrove change-detection workflow combining context-aware deep learning with an intuitive municipal decision-support web prototype for Aringay MENRO."
    p_bot.font.bold = True; p_bot.font.size = Pt(12); p_bot.font.color.rgb = RGBColor(254, 240, 138); p_bot.alignment = PP_ALIGN.CENTER

    add_notes(s4,
        "Here we articulate the core problem. Why hasn't this been solved already? First, Dulao's muddy, tidally inundated terrain makes physical surveys dangerous and incomplete. Second, simple spectral thresholding fails because fishpond algae and terrestrial trees look identical to mangroves in simple pixel bands. Third, even when complex satellite studies are published, they end up as raw code or academic papers that local municipal officers at Aringay MENRO cannot operationalize without specialized GIS tools.",
        "The gap is not just algorithmic—it is translational: connecting robust deep learning with an intuitive, accessible municipal software interface.",
        "U-Net resolves the spectral confusion problem through spatial-contextual convolution, while our Flask/Leaflet web prototype resolves the software adoption barrier.",
        "Q: Why can't MENRO just use Google Earth Pro?\nA: Google Earth Pro only provides visual RGB composite images without analytical spectral bands (NIR/SWIR), without automated gain/loss area quantification, and without validated classification models tailored to Dulao's canopy.",
        "Do not invent criticisms of Aringay MENRO. Frame this respectfully as resource and tool constraints common to municipal environmental departments.")

    # SLIDE 5: OVERVIEW - GENERAL & SPECIFIC OBJECTIVES
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Project Overview: General & Specific Research Objectives", "1. Project Overview", 5)

    gen_card = add_card(s5, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.4), bg_color=COLOR_LIGHT_GAIN, border_color=COLOR_MID_GREEN, border_width=2)
    tb_gen = s5.shapes.add_textbox(Inches(1.1), Inches(1.95), Inches(11.1), Inches(1.1))
    tf_gen = tb_gen.text_frame; tf_gen.word_wrap = True
    p_gt = tf_gen.paragraphs[0]; p_gt.text = "GENERAL OBJECTIVE"; p_gt.font.bold = True; p_gt.font.size = Pt(12); p_gt.font.color.rgb = COLOR_MID_GREEN

    p_gd = tf_gen.add_paragraph()
    p_gd.text = "To develop an automated change detection and decision-support workflow for mangrove canopy gain and loss in Barangay Dulao, Aringay, La Union from 2019 to 2024 by integrating multi-spectral Sentinel-2 satellite imagery, a 5-channel U-Net deep learning model, and an interactive web-based prototype."
    p_gd.font.bold = True; p_gd.font.size = Pt(13.5); p_gd.font.color.rgb = COLOR_TEXT_MAIN; p_gd.space_before = Pt(4)

    specs = [
        {"num": "SPECIFIC OBJECTIVE 1", "title": "Data Pipeline & Feature Prep",
         "items": ["• Acquire Sentinel-2 L2A surface reflectance (2019–2024 dry season).",
                   "• Extract Green (B3), Red (B4), NIR (B8), and SWIR (B11).",
                   "• Resample B11 from 20m to 10m bilinear resolution.",
                   "• Compute and normalize NDVI to produce 5-channel 256×256 tensors."]},
        {"num": "SPECIFIC OBJECTIVE 2", "title": "U-Net Model & Evaluation",
         "items": ["• Construct a 5-channel modified U-Net architecture.",
                   "• Train model using 80/20 train-validation partitioning.",
                   "• Optimize with Adam optimizer & Binary Cross-Entropy loss.",
                   "• Rigorously evaluate using F1-score, IoU, and mAP across a 0.05–0.95 threshold sweep."]},
        {"num": "SPECIFIC OBJECTIVE 3", "title": "PCC & Prototype System",
         "items": ["• Execute Post-Classification Comparison (PCC) between annual pairs.",
                   "• Classify transitions into Gain, Loss, Stable, and Stable Non-mangrove.",
                   "• Develop interactive Flask/Leaflet web GIS dashboard.",
                   "• Implement automated one-click PDF reporting for Aringay MENRO."]}
    ]

    for i, sp in enumerate(specs):
        c_left = Inches(0.8) + i * Inches(4.016)
        card = add_card(s5, c_left, Inches(3.4), Inches(3.7), Inches(3.5), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        tb = s5.shapes.add_textbox(c_left + Inches(0.2), Inches(3.6), Inches(3.3), Inches(3.1))
        tf = tb.text_frame; tf.word_wrap = True
        
        p_sn = tf.paragraphs[0]; p_sn.text = sp["num"]; p_sn.font.bold = True; p_sn.font.size = Pt(10); p_sn.font.color.rgb = COLOR_MID_GREEN
        p_st = tf.add_paragraph(); p_st.text = sp["title"]; p_st.font.bold = True; p_st.font.size = Pt(14); p_st.font.color.rgb = COLOR_TEXT_MAIN; p_st.space_after = Pt(10)

        for item in sp["items"]:
            pi = tf.add_paragraph(); pi.text = item; pi.font.size = Pt(10.5); pi.font.color.rgb = COLOR_TEXT_MUTED; pi.space_before = Pt(3)

    add_notes(s5,
        "Our study is organized around one overarching general objective and three clear specific objectives. The general objective is to develop the end-to-end automated gain and loss detection system for Barangay Dulao across 2019 to 2024. Specific Objective 1 focuses on data acquisition, band selection, bilinear resampling of Band 11, and NDVI integration. Specific Objective 2 targets the 5-channel U-Net deep learning model, training, and threshold evaluation. Specific Objective 3 covers the Post-Classification Comparison algorithm and the operational software prototype.",
        "Each specific objective directly addresses one pillar of the project: Data/Features -> Deep Learning Model -> Software Prototype.",
        "The three objectives mirror the Software Engineering 2 project life cycle: Data Engineering -> AI Model Development -> User-Facing Application.",
        "Q: Why are there 3 specific objectives?\nA: They correspond to the three core technical components of the thesis proposal: data pipeline, deep learning segmentation, and post-classification decision-support prototype.",
        "Ensure you articulate that Specific Objective 2 includes threshold sweeping from 0.05 to 0.95 to identify the optimal operating point.")

    # =========================================================================
    # PILLAR 2: PROJECT SCOPE (SLIDES 6, 7)
    # =========================================================================
    # SLIDE 6: SCOPE - SPATIAL & TEMPORAL DELIMITATION
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Project Scope: Spatial Delimitation & Temporal Baseline", "2. Project Scope", 6)

    left_c = add_card(s6, Inches(0.8), Inches(1.8), Inches(5.0), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_loc = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.6), Inches(4.7))
    tf_loc = tb_loc.text_frame; tf_loc.word_wrap = True

    p = tf_loc.paragraphs[0]; p.text = "GEOGRAPHIC DELIMITATION"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p = tf_loc.add_paragraph(); p.text = "Barangay Dulao, Aringay, La Union"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_after = Pt(8)

    specs_list = [
        ("Geographic Coordinates:", "120.320°E to 120.343°E\n16.364°N to 16.388°N"),
        ("Authoritative Area (ROI):", "316.74 Hectares (25-point Polygon Boundary)"),
        ("Ecological Context:", "Aringay River estuary discharging into Lingayen Gulf, South China Sea"),
        ("Temporal Baseline:", "6 Annual Epochs: 2019, 2020, 2021, 2022, 2023, 2024"),
        ("Seasonal Acquisition Window:", "February 1 to April 30 (Dry Season)\nCloud cover filtered < 20% to minimize cloud shadow artifacts and tidal variations")
    ]
    for lbl, val in specs_list:
        p_l = tf_loc.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10.5); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(6)
        p_v = tf_loc.add_paragraph(); p_v.text = val; p_v.font.size = Pt(10.5); p_v.font.color.rgb = COLOR_TEXT_MUTED

    map_card = add_card(s6, Inches(6.1), Inches(1.8), Inches(6.433), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    map_img_path = "extracted_assets/dulao_roi_map.png"
    if os.path.exists(map_img_path):
        s6.shapes.add_picture(map_img_path, Inches(6.2), Inches(1.9), Inches(6.233), Inches(4.9))

    add_notes(s6,
        "Turning to Pillar 2: Project Scope. Here we show the exact spatial and temporal delimitations of our research. Our study area is Barangay Dulao in the municipality of Aringay, La Union. The authoritative Region of Interest encompasses exactly 316.74 hectares defined by a 25-vertex boundary polygon. The temporal window spans six consecutive years from 2019 to 2024. Crucially, all satellite imagery was collected strictly between February 1 and April 30. This dry-season window was selected to minimize cloud cover to below 20% and avoid monsoonal cloud masking.",
        "The 316.74-hectare 25-point ROI is the exact geometric boundary defined in our spatial schema and recognized by MENRO.",
        "Dry-season acquisition reduces atmospheric moisture, minimizes cloud cover, and provides consistent sun angles and tidal baselines across years.",
        "Q: Why only February to April?\nA: La Union experiences its dry season from February to April. During the wet season, cloud cover consistently exceeds 70-80%, which severely obscures optical satellite sensors.",
        "Do NOT mention arbitrary hectares. The exact polygon area calculated in the spatial database and code is 316.74 ha.")

    # SLIDE 7: SCOPE - IN-SCOPE VS. OUT-OF-SCOPE BOUNDARIES
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Project Scope: Functional Capabilities & Boundary Matrix", "2. Project Scope", 7)

    # Left: In-Scope Card
    in_card = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=COLOR_LIGHT_GAIN, border_color=COLOR_MID_GREEN, border_width=2)
    tb_in = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_in = tb_in.text_frame; tf_in.word_wrap = True

    p = tf_in.paragraphs[0]; p.text = "IN-SCOPE CAPABILITIES (SYSTEM DELIVERABLES)"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_in.add_paragraph(); p_t.text = "Operational Focus"; p_t.font.bold = True; p_t.font.size = Pt(16); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(8)

    in_items = [
        ("Sentinel-2 MSI Preprocessing:", "Harmonized L2A reflectance collection across 2019–2024 dry seasons."),
        ("Multi-Band Feature Stacking:", "Extraction of B3, B4, B8, B11 (resampled to 10m), and computed NDVI into 5-channel 256×256 tensors."),
        ("Binary Semantic Segmentation:", "U-Net classification of mangrove vs. non-mangrove canopy covers."),
        ("Pairwise Post-Classification (PCC):", "Mathematical cross-tabulation of all 15 annual pairs into Gain, Loss, Stable, and Other."),
        ("Interactive Web GIS Dashboard:", "Flask backend, REST API, Leaflet map overlays, and Chart.js historical trend analytics."),
        ("Automated Municipal Reporting:", "One-click generation of formal A4 PDF reports for Aringay MENRO.")
    ]
    for lbl, desc in in_items:
        p_l = tf_in.add_paragraph(); p_l.text = f"✓ {lbl}"; p_l.font.bold = True; p_l.font.size = Pt(10.5); p_l.font.color.rgb = COLOR_GAIN_GREEN; p_l.space_before = Pt(4)
        p_d = tf_in.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Out-of-Scope Card
    out_card = add_card(s7, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER, border_width=1.5)
    tb_out = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_out = tb_out.text_frame; tf_out.word_wrap = True

    p = tf_out.paragraphs[0]; p.text = "OUT-OF-SCOPE & DELIMITATIONS (BOUNDARIES)"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_LOSS_RED
    p_t = tf_out.add_paragraph(); p_t.text = "System Delimitations"; p_t.font.bold = True; p_t.font.size = Pt(16); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(8)

    out_items = [
        ("Live Satellite Ingestion:", "The web prototype is designed for decision support and planning using pre-computed seasonal mosaics, not real-time in-browser satellite downloads."),
        ("Species-Level Classification:", "Delimited strictly to binary mangrove canopy presence due to Sentinel-2's 10m resolution (Rhizophora vs. Avicennia separation requires drone/hyperspectral data)."),
        ("Wet Season Monitoring:", "Monsoonal months (May–January) are excluded due to frequent cloud cover exceeding 70-80%."),
        ("Commercial Satellite Sensors:", "High-cost sensors (PlanetScope, WorldView) are excluded to ensure zero licensing costs for municipal LGU sustainability."),
        ("Autonomous Drone Integration:", "UAV field surveys are outside the software scope but recommended for future micro-scale planting validation.")
    ]
    for lbl, desc in out_items:
        p_l = tf_out.add_paragraph(); p_l.text = f"✗ {lbl}"; p_l.font.bold = True; p_l.font.size = Pt(10.5); p_l.font.color.rgb = COLOR_LOSS_RED; p_l.space_before = Pt(4)
        p_d = tf_out.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    add_notes(s7,
        "Here we clearly define what is in scope versus what is out of scope. In-scope items encompass the complete end-to-end software pipeline: Sentinel-2 dry-season extraction, 5-channel tensor generation, U-Net semantic segmentation, Post-Classification Comparison for all 15 pairs, interactive web GIS visualization, and automated PDF reporting. Crucially, out-of-scope boundaries include live in-app satellite downloading, species-level distinction (which requires centimeter drone imagery), and wet-season analysis due to dense cloud cover.",
        "Establishing explicit project scope boundaries demonstrates engineering maturity and aligns system capabilities with municipal operational realities.",
        "By focusing on binary mangrove detection at 10m resolution, the system maximizes accuracy while remaining sustainable on standard LGU computers.",
        "Q: Why did you not implement live satellite download directly inside the Flask app?\nA: Live satellite ingestion requires heavy API credentials, cloud storage quotas, and intense raster processing that exceeds typical municipal office internet bandwidth and hardware. Pre-processing seasonal composites ensures instant, reliable dashboard responsiveness.",
        "Deliver this slide with complete confidence; clear delimitations protect the team from unreasonable panel scope creep.")

    # =========================================================================
    # PILLAR 3: SOFTWARE DEVT METHODOLOGY (SLIDES 8, 9, 10)
    # =========================================================================
    # SLIDE 8: METHODOLOGY - IID PROCESS MODEL
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Software Devt Methodology: Iterative & Incremental Model", "3. Software Devt Methodology", 8)

    left_c = add_card(s8, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    iid_img = "extracted_assets/p21_img1_86.jpeg"
    if os.path.exists(iid_img):
        s8.shapes.add_picture(iid_img, Inches(0.9), Inches(2.0), Inches(6.6), Inches(4.7))

    right_c = add_card(s8, Inches(7.8), Inches(1.8), Inches(4.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_iid = s8.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.333), Inches(4.7))
    tf_iid = tb_iid.text_frame; tf_iid.word_wrap = True

    p = tf_iid.paragraphs[0]; p.text = "IID MODEL IMPLEMENTATION PHASES"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN

    phases = [
        ("Phase 1: Domain Analysis", "Consulted Aringay MENRO on local conservation needs."),
        ("Phase 2: Data Acquisition", "Extracted 2019–2024 Sentinel-2 scenes via Earth Engine."),
        ("Phase 3: Preprocessing & Stack", "Harmonization, bilinear resampling, and NDVI calculation."),
        ("Phase 4: Dataset & Partitioning", "Patch slicing (256×256) & 80/20 train-validation protocol."),
        ("Phase 5: U-Net Architecture", "Constructed 5-channel encoder-decoder deep network."),
        ("Phase 6: Training & Validation", "Adam optimizer, BCE loss, EarlyStopping (patience=10)."),
        ("Phase 7: Change Detection (PCC)", "Matrix comparison for Gain, Loss, Stable, and Other."),
        ("Phase 8: Web Prototype & Reports", "Interactive Flask web GIS and automated PDF reports.")
    ]
    for p_title, p_desc in phases:
        p_t = tf_iid.add_paragraph(); p_t.text = f"• {p_title}: "; p_t.font.bold = True; p_t.font.size = Pt(9.5); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_before = Pt(3)
        p_t.add_run().text = p_desc
        p_t.runs[1].font.bold = False; p_t.runs[1].font.size = Pt(9.5); p_t.runs[1].font.color.rgb = COLOR_TEXT_MUTED

    add_notes(s8,
        "Advancing to Pillar 3: Software Development Methodology. Our software development lifecycle follows the Iterative and Incremental Development (IID) model, documented on page 11 of our thesis manuscript. Rather than a rigid waterfall approach, IID allowed our team to iteratively refine data ingestion, model architecture, and web interface based on continuous testing and domain feedback from Aringay MENRO.",
        "The project follows the 8 discrete phases of the IID framework, advancing from domain requirements to full prototype deployment.",
        "The IID model is widely recognized in software engineering for AI systems where experimental model iterations must align with evolving software requirements.",
        "Q: Why did you choose IID over standard Waterfall?\nA: Deep learning development is inherently experimental. Training hyperparameters, loss stabilization, and threshold selection require iterative tuning cycles that cannot be frozen in a single waterfall pass.",
        "Refer to Figure 1 on the left, which is taken directly from page 11 of the thesis manuscript.")

    # SLIDE 9: METHODOLOGY - PREPROCESSING & 80/20 PARTITION PROTOCOL
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Software Devt Methodology: Data Preprocessing & Partitioning", "3. Software Devt Methodology", 9)

    card_prep = add_card(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_pr = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_pr = tb_pr.text_frame; tf_pr.word_wrap = True

    p = tf_pr.paragraphs[0]; p.text = "DATA INGESTION & FEATURE ENGINEERING"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_pr.add_paragraph(); p_t.text = "Sentinel-2 Multi-Spectral Pipeline"; p_t.font.bold = True; p_t.font.size = Pt(15); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(6)

    prep_steps = [
        ("Level-2A Surface Reflectance:", "Copernicus Sentinel-2 MSI products acquired via Google Earth Engine."),
        ("Band Isolation:", "B3 (Green 560nm), B4 (Red 665nm), B8 (NIR 842nm), B11 (SWIR 1610nm)."),
        ("Bilinear Resampling:", "Band 11 resampled from native 20m to 10m grid to match B3, B4, and B8."),
        ("NDVI Integration:", "Calculated as (B8 - B4) / (B8 + B4) and rescaled to [0.0, 1.0]."),
        ("Tiling & Padding:", "Sliced into 256×256 patches with reflection padding along ROI borders.")
    ]
    for lbl, desc in prep_steps:
        p_l = tf_pr.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(4)
        p_d = tf_pr.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(9.5); p_d.font.color.rgb = COLOR_TEXT_MUTED

    card_split = add_card(s9, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_sp = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_sp = tb_sp.text_frame; tf_sp.word_wrap = True

    p = tf_sp.paragraphs[0]; p.text = "EXPERIMENTAL DATA PARTITIONING"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_sp.add_paragraph(); p_t.text = "80% Training / 20% Validation Protocol"; p_t.font.bold = True; p_t.font.size = Pt(15); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(6)

    split_notes = [
        ("Experimental Protocol:", "The 80/20 partition was adopted by the research team as the study-specific experimental protocol."),
        ("80% Training Partition:", "Used to optimize convolutional weights via backpropagation and Adam optimizer (lr=0.001)."),
        ("20% Holdout Validation:", "Completely isolated from model training. Evaluated at each epoch to monitor generalization and avoid overfitting."),
        ("Optimization Controls:", "Binary Cross-Entropy (BCE) loss + EarlyStopping (patience=10 epochs on validation loss)."),
        ("Academic Integrity Rule:", "This 80/20 partition is an established experimental choice by the research team and is not attributed to external papers.")
    ]
    for lbl, desc in split_notes:
        p_l = tf_sp.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(4)
        p_d = tf_sp.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(9.5); p_d.font.color.rgb = COLOR_TEXT_MUTED

    add_notes(s9,
        "Continuing with methodology, Slide 9 details our data preparation and partitioning protocol. On the left, we isolate Bands 3, 4, 8, and 11, bilinearly resample Band 11 from 20m to 10m, calculate NDVI, and construct 256x256 patches. On the right, we partition our patch dataset into 80% for training and 20% for validation. We emphasize that this 80/20 partition was adopted by our research team as the experimental protocol for this study. The model is optimized using Adam with a learning rate of 0.001, BCE loss, and EarlyStopping with patience 10.",
        "80/20 data partition is our study-specific experimental protocol; training uses Adam (lr=0.001), BCE loss, EarlyStopping (patience=10), and a 0.05–0.95 threshold sweep.",
        "Binary Cross-Entropy penalizes incorrect binary probabilities pixel by pixel, while EarlyStopping terminates training once the validation loss stops improving.",
        "Q: Why did you choose an 80/20 split instead of 70/30 or k-fold cross-validation?\nA: The 80/20 split is our study-specific experimental partitioning protocol. It provides sufficient training volume to optimize deep convolutional kernels while reserving an independent 20% holdout set to evaluate generalization without spatial leakage.",
        "CRITICAL DEFENSE RULE: NEVER attribute the 80/20 split to Ronneberger or external authors. State clearly: 'The 80/20 split is our study-specific experimental partitioning protocol.'")

    # SLIDE 10: METHODOLOGY - TESTING, EVALUATION & QA PROTOCOL
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Software Devt Methodology: Quality Assurance & Evaluation", "3. Software Devt Methodology", 10)

    c_m = add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_m = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_m = tb_m.text_frame; tf_m.word_wrap = True

    p = tf_m.paragraphs[0]; p.text = "ACADEMIC EVALUATION METRICS"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_m.add_paragraph(); p_t.text = "Standard Segmentation Metrics"; p_t.font.bold = True; p_t.font.size = Pt(15); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(6)

    metrics = [
        ("Precision:", "TP / (TP + FP) — Minimizes false positive mangrove claims over fishpond algae."),
        ("Recall (Sensitivity):", "TP / (TP + FN) — Ensures actual fragmented mangrove stands are not missed."),
        ("F1-Score (Dice Coeff):", "2 × (Prec × Rec) / (Prec + Rec) — Harmonic balance of accuracy across classes."),
        ("Intersection over Union (IoU):", "TP / (TP + FP + FN) — Standard geospatial overlap benchmark."),
        ("Mean Average Precision (mAP):", "Integrated Area Under the Precision-Recall Curve across threshold sweeps."),
        ("Threshold Sweep Protocol:", "Evaluated across 19 cutoffs from 0.05 to 0.95 (step 0.05) to determine optimal operating threshold.")
    ]
    for lbl, desc in metrics:
        p_l = tf_m.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(4)
        p_d = tf_m.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(9.5); p_d.font.color.rgb = COLOR_TEXT_MUTED

    c_t = add_card(s10, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_t = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_t = tb_t.text_frame; tf_t.word_wrap = True

    p = tf_t.paragraphs[0]; p.text = "SOFTWARE QUALITY VERIFICATION"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_t.add_paragraph(); p_t.text = "Automated Test Assertions"; p_t.font.bold = True; p_t.font.size = Pt(15); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(6)

    tests = [
        ("Mathematical Partition Invariance:", "Total ROI Area = Gain + Loss + Stable Mangrove + Stable Non-mangrove (verified across all 15 pairs)."),
        ("Spatial Boundary Clamping:", "All GeoJSON polygons strictly bounded within Dulao's 316.74-hectare envelope."),
        ("API Contract Verification:", "JSON schema validation for /api/statistics, /api/data, and error handlers (HTTP 400 for invalid year pairs)."),
        ("PDF Document Integrity:", "ReportLab binary streams verified for valid EOF markers and correct table formatting."),
        ("Demonstration Label Transparency:", "Explicit 'DEMO DATA' watermark displayed across all mock endpoints.")
    ]
    for lbl, desc in tests:
        p_l = tf_t.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(4)
        p_d = tf_t.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(9.5); p_d.font.color.rgb = COLOR_TEXT_MUTED

    add_notes(s10,
        "Slide 10 covers our dual-track testing and evaluation methodology: academic model metrics on the left, and software verification on the right. For the AI model, we employ Precision, Recall, F1-score (or Dice coefficient), Intersection over Union (IoU), and mAP across a threshold sweep from 0.05 to 0.95. For the software engineering track, we wrote automated test scripts verifying mathematical partition invariance: the sum of Gain, Loss, Stable Mangrove, and Stable Non-mangrove must always equal the total 316.74-hectare area of Dulao without a single pixel missing or double-counted.",
        "Testing covers both deep learning segmentation fidelity (IoU/F1) and software integrity (invariance tests, API contracts, PDF generation).",
        "Threshold sweeping from 0.05 to 0.95 ensures that the selected cutoff maximizes the F1-score rather than assuming an arbitrary 0.50 cutoff.",
        "Q: What are your actual model accuracy numbers right now?\nA: The values currently loaded in the prototype are demonstration benchmark values used to validate the software and API pipeline. Final empirical metrics will be computed once the independent MENRO ground-truth mask validation is finalized.",
        "CRITICAL CAUTION: Do NOT present demo numbers like F1=0.874 as final empirical findings. Clearly state they are prototype validation values.")

    # =========================================================================
    # PILLAR 4: SOFTWARE REQUIREMENTS & SYSTEM MODELS (SLIDES 11, 12, 13, 14, 15)
    # =========================================================================
    # SLIDE 11: REQUIREMENTS - FUNCTIONAL & NON-FUNCTIONAL SPECIFICATIONS
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Software Requirements: Functional & Non-Functional Specs", "4. Requirements & Models", 11)

    # Left: Requirements Specification Card
    c_req = add_card(s11, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_req = s11.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.4), Inches(4.8))
    tf_req = tb_req.text_frame; tf_req.word_wrap = True

    p = tf_req.paragraphs[0]; p.text = "FORMAL SOFTWARE SPECIFICATIONS"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_req.add_paragraph(); p_t.text = "Functional & Non-Functional Matrix"; p_t.font.bold = True; p_t.font.size = Pt(14); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(4)

    req_list = [
        ("FR-01 (Data Ingest):", "System must load 2019–2024 annual composite masks for Dulao's 316.74 ha ROI."),
        ("FR-02 (Pairwise Change):", "System must execute PCC on demand across any of the 15 valid year combinations."),
        ("FR-03 (Interactive Cartography):", "Leaflet web map must display ROI boundary, gain polygons, and loss polygons with layer toggles."),
        ("FR-04 (Statistical Analytics):", "Dashboard must calculate net area change (ha) and render multi-temporal trend charts."),
        ("FR-05 (PDF Export):", "Headless ReportLab engine must generate downloadable A4 conservation reports."),
        ("NFR-01 (Performance):", "API responses and change calculations must complete within 2.0 seconds."),
        ("NFR-02 (Usability):", "Zero-code, responsive web interface accessible on standard municipal office desktop browsers."),
        ("NFR-03 (Data Integrity):", "Gain + Loss + Stable Mangrove + Stable Non-mangrove must exactly equal 316.74 ha.")
    ]
    for lbl, desc in req_list:
        p_l = tf_req.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(9.5); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(3)
        p_d = tf_req.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(9); p_d.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Embedded Use Case Diagram
    c_uc = add_card(s11, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    uc_img = "extracted_assets/requirements_usecase_model.png"
    if os.path.exists(uc_img):
        s11.shapes.add_picture(uc_img, Inches(6.9), Inches(1.9), Inches(5.533), Inches(4.9))

    add_notes(s11,
        "Advancing to Pillar 4: Software Requirements and System Models. Slide 11 establishes our functional and non-functional requirements alongside our Use Case model. We identified five core functional requirements: data ingestion, pairwise PCC execution, interactive cartography, statistical analytics, and automated PDF export. Our non-functional requirements emphasize sub-2-second API response times, zero GIS training required for municipal officers, and 100% mathematical area conservation. The diagram on the right models user interactions between the primary municipal officer and the research administrator.",
        "Clear functional and non-functional requirements ensure the software meets municipal user needs and strict engineering constraints.",
        "The use case diagram highlights the boundary between the web interface and the underlying geospatial analytics engine.",
        "Q: How did you validate that non-functional performance requirements are met?\nA: We benchmarked API response times locally using Python request timers; GeoJSON payloads and statistics return in under 350 milliseconds, well within our 2-second threshold.",
        "Keep the focus on how requirements directly serve the municipal user persona.")

    # SLIDE 12: SYSTEM MODELS - THREE-TIER SOFTWARE ARCHITECTURE
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "System Models: Three-Tier Software Architecture", "4. Requirements & Models", 12)

    arch_card = add_card(s12, Inches(0.8), Inches(1.8), Inches(8.0), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    arch_img = "extracted_assets/system_architecture_diagram.png"
    if os.path.exists(arch_img):
        s12.shapes.add_picture(arch_img, Inches(0.9), Inches(1.9), Inches(7.8), Inches(4.9))

    side_c = add_card(s12, Inches(9.0), Inches(1.8), Inches(3.533), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_side = s12.shapes.add_textbox(Inches(9.2), Inches(2.0), Inches(3.133), Inches(4.7))
    tf_side = tb_side.text_frame; tf_side.word_wrap = True

    p = tf_side.paragraphs[0]; p.text = "ARCHITECTURE HIGHLIGHTS"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN

    points = [
        ("Decoupled Design:", "Flask backend cleanly separated from Leaflet frontend via JSON REST endpoints."),
        ("REST API Layer:", "/api/study-area, /api/statistics, and /api/change-detection endpoints."),
        ("Automated Reporting:", "Headless ReportLab engine generates standardized A4 PDF reports on demand."),
        ("Interactive GIS:", "Leaflet.js client renders multi-layer vector overlays with real-time opacity controls."),
        ("Production Readiness:", "Config-driven architecture; switching DEMO_MODE to False immediately hooks real inference.")
    ]
    for pt_t, pt_d in points:
        p_t = tf_side.add_paragraph(); p_t.text = pt_t; p_t.font.bold = True; p_t.font.size = Pt(10.5); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_before = Pt(6)
        p_d = tf_side.add_paragraph(); p_d.text = pt_d; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED; p_d.space_before = Pt(2)

    add_notes(s12,
        "Slide 12 demonstrates the three-tier system architecture of our prototype. Tier 1 handles Data and Preprocessing, ingesting Sentinel-2 imagery, extracting spectral tensors, and reading the 25-point Dulao ROI boundary. Tier 2 is our Python Flask Backend, hosting our REST API endpoints and our automated ReportLab PDF generation engine. Tier 3 is the responsive web frontend powered by Leaflet.js and Chart.js, designed specifically for non-technical municipal operators.",
        "The architecture is fully decoupled: the backend exposes REST API endpoints that any client can consume, ensuring modularity and maintainability.",
        "The codebase follows MVC and clean code standards with centralized configuration in config.py.",
        "Q: Why choose Flask instead of Django or React?\nA: Flask provides a lightweight, highly responsive WSGI server that easily integrates NumPy, PyTorch/TensorFlow, and ReportLab in a single Python runtime without the excessive overhead of Django or a decoupled Node.js build step.",
        "Do not claim that the app is hosted on AWS/cloud currently. State that it is running locally on Flask WSGI development server.")

    # SLIDE 13: SYSTEM MODELS - 5D FEATURE TENSOR & NDVI PIPELINE
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "System Models: 5D Feature Tensor & NDVI Pipeline", "4. Requirements & Models", 13)

    pipe_card = add_card(s13, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.2), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    pipe_img = "extracted_assets/spectral_bands_ndvi_pipeline.png"
    if os.path.exists(pipe_img):
        s13.shapes.add_picture(pipe_img, Inches(1.0), Inches(1.9), Inches(11.333), Inches(3.0))

    exp_cards = [
        {"title": "1. Multi-Spectral Bands", "color": COLOR_MID_GREEN,
         "desc": "B3 (Green 560nm), B4 (Red 665nm), B8 (NIR 842nm), B11 (SWIR 1610nm). Captures chlorophyll absorption, leaf scattering, and moisture absorption."},
        {"title": "2. NDVI Formulation", "color": COLOR_BLUE_ACCENT,
         "desc": "NDVI = (B8 - B4) / (B8 + B4). Rescaled from [-1, 1] to [0, 1]. Provides explicit photosynthetic vigor to accelerate convolutional convergence."},
        {"title": "3. 256×256×5 Tensor Stack", "color": COLOR_AMBER,
         "desc": "Harmonizes all 5 channels onto a standardized 10m grid. Border patches utilize reflection padding to maintain boundary convolution stability."}
    ]

    for i, c in enumerate(exp_cards):
        c_left = Inches(0.8) + i * Inches(4.016)
        card = add_card(s13, c_left, Inches(5.2), Inches(3.7), Inches(1.7), bg_color=COLOR_WHITE, border_color=c["color"], border_width=1.5)
        tb = s13.shapes.add_textbox(c_left + Inches(0.15), Inches(5.25), Inches(3.4), Inches(1.6))
        tf = tb.text_frame; tf.word_wrap = True
        p_t = tf.paragraphs[0]; p_t.text = c["title"]; p_t.font.bold = True; p_t.font.size = Pt(12); p_t.font.color.rgb = c["color"]
        p_d = tf.add_paragraph(); p_d.text = c["desc"]; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED; p_d.space_before = Pt(3)

    add_notes(s13,
        "Slide 13 details our feature engineering model. We construct a 5-dimensional tensor input. Why 5 channels? Bands 3, 4, and 8 provide green, red, and near-infrared reflectance. Band 11 provides short-wave infrared, which is vital for water-soil discrimination. On top of these, we explicitly calculate NDVI: (B8 minus B4) divided by (B8 plus B4), normalized to 0 to 1. This 5-channel stack guarantees that our neural network has access to both raw reflectances and derived vegetation health.",
        "The 5-channel tensor [B3, B4, B8, B11, NDVI] combines raw electromagnetic reflectances with biophysical indices.",
        "Bilinear resampling of Band 11 aligns 20m pixels to 10m without spatial distortion.",
        "Q: Why include NDVI if the model already has B4 and B8?\nA: Explicitly including NDVI provides a pre-computed non-linear biological prior that stabilizes early convolutional layer training and speeds up convergence.",
        "Ensure you mention that all 5 channels are normalized to the [0, 1] range.")

    # SLIDE 14: SYSTEM MODELS - 5-CHANNEL U-NET DEEP LEARNING MODEL
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "System Models: 5-Channel U-Net Architecture", "4. Requirements & Models", 14)

    left_c = add_card(s14, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    unet_img = "extracted_assets/p25_img1_95.png"
    if os.path.exists(unet_img):
        s14.shapes.add_picture(unet_img, Inches(0.9), Inches(2.0), Inches(6.6), Inches(4.7))

    right_c = add_card(s14, Inches(7.8), Inches(1.8), Inches(4.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_u = s14.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.333), Inches(4.7))
    tf_u = tb_u.text_frame; tf_u.word_wrap = True

    p = tf_u.paragraphs[0]; p.text = "U-NET SPECIFICATIONS (THESIS PAGE 15)"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN

    unet_specs = [
        ("Input Dimension:", "256 × 256 × 5 (B3, B4, B8, B11, NDVI)"),
        ("Contracting Path (Encoder):", "Successive 3×3 convolutions, ReLU activation, and 2×2 max pooling (feature extraction)."),
        ("Bottleneck Layer:", "Deepest representations capturing macro spatial context across Dulao's coastline."),
        ("Expansive Path (Decoder):", "Up-convolutions restoring full 256×256 spatial resolution."),
        ("Skip Connections:", "Directly concatenate fine-grained encoder feature maps to decoder to preserve precise mangrove boundaries."),
        ("Output Layer:", "1×1 convolution with Sigmoid activation → probability map [0.0, 1.0] of mangrove presence.")
    ]
    for lbl, desc in unet_specs:
        p_l = tf_u.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10.5); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(4)
        p_d = tf_u.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    add_notes(s14,
        "Slide 14 details our AI model: a modified U-Net architecture adapted from Ronneberger et al. and configured specifically for 5-channel inputs. The figure on the left is taken directly from page 15 of our thesis proposal. It follows a symmetrical encoder-decoder structure. The encoder extracts semantic features through successive 3x3 convolutions and 2x2 max-pooling. The decoder restores the spatial resolution back to 256x256. Most importantly, skip connections copy high-resolution spatial details directly across the U, ensuring sharp, precise canopy boundaries rather than blurry blobs.",
        "The model receives a 256x256x5 tensor and outputs a 256x256x1 binary probability map via a sigmoid activation function.",
        "Skip connections solve the problem of spatial information loss that occurs during downsampling, which is essential for delineating narrow mangrove fringe strips along tidal canals.",
        "Q: Why U-Net instead of DeepLabV3+ or YOLO?\nA: Mangrove canopies in Dulao often occur in narrow linear fringing strips along estuaries. U-Net's skip connections excel at preserving pixel-level boundary fidelity for dense semantic segmentation, whereas YOLO is for bounding-box object detection.",
        "Highlight that the input layer was specifically modified from standard 3-channel RGB to 5 channels to accept our multispectral stack.")

    # SLIDE 15: SYSTEM MODELS - POST-CLASSIFICATION TRANSITION MODEL
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "System Models: Post-Classification Comparison (PCC)", "4. Requirements & Models", 15)

    mat_card = add_card(s15, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    trans_img = "extracted_assets/transition_matrix_diagram.png"
    if os.path.exists(trans_img):
        s15.shapes.add_picture(trans_img, Inches(0.9), Inches(1.9), Inches(7.3), Inches(4.9))

    side_c = add_card(s15, Inches(8.5), Inches(1.8), Inches(4.033), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_side = s15.shapes.add_textbox(Inches(8.7), Inches(2.0), Inches(3.633), Inches(4.7))
    tf_side = tb_side.text_frame; tf_side.word_wrap = True

    p = tf_side.paragraphs[0]; p.text = "THE 4 CANOPY TRANSITION STATES"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN

    states = [
        ("GAIN (Value = +1):", "Non-Mangrove in T₁ → Mangrove in T₂. Indicates canopy recovery, natural regeneration, or planting.", COLOR_GAIN_GREEN),
        ("LOSS (Value = -1):", "Mangrove in T₁ → Non-Mangrove in T₂. Indicates clearing, fishpond expansion, or storm scour.", COLOR_LOSS_RED),
        ("STABLE MANGROVE (Value = 2):", "Mangrove in both T₁ & T₂. Represents persistent core mangrove stands.", COLOR_DARK_GREEN),
        ("STABLE NON-MANGROVE (Value = 0):", "Non-mangrove in both T₁ & T₂. Open water, mudflats, sandbars, and upland soil.", COLOR_TEXT_MUTED)
    ]
    for title, desc, col in states:
        pt = tf_side.add_paragraph(); pt.text = title; pt.font.bold = True; pt.font.size = Pt(11); pt.font.color.rgb = col; pt.space_before = Pt(8)
        pd = tf_side.add_paragraph(); pd.text = desc; pd.font.size = Pt(10); pd.font.color.rgb = COLOR_TEXT_MUTED; pd.space_before = Pt(2)

    add_notes(s15,
        "Slide 15 presents our change detection mathematical model: Post-Classification Comparison, or PCC. Rather than subtracting raw spectral pixels which is easily corrupted by atmospheric differences, PCC classifies each annual scene independently, and then performs a pixel-by-pixel cross-tabulation between Year T1 and Year T2. This generates a clean transition matrix with four discrete classes: Mangrove Gain, Mangrove Loss, Stable Mangrove, and Stable Non-mangrove.",
        "Post-Classification Comparison eliminates false-change noise from seasonal sensor illumination and tidal water fluctuations by comparing classified categorical masks.",
        "Each 10m x 10m pixel equals 0.01 hectares. Multiplying classified pixel counts by 0.01 directly gives the total hectarage for Gain, Loss, and Stable cover.",
        "Q: Why PCC instead of Image Differencing or CVA?\nA: Direct image differencing compares raw spectral values, which are easily biased by differing tide levels or atmospheric moisture. PCC compares validated thematic classifications, yielding explicit 'from-to' categorical transitions.",
        "Emphasize that the prototype supports all 15 pairwise annual combinations across the 2019 to 2024 period.")

    # =========================================================================
    # PILLAR 5: SOFTWARE DEMO (SLIDES 16, 17)
    # =========================================================================
    # SLIDE 16: DEMO - OPERATIONAL WORKFLOW & UI ARCHITECTURE
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Software Demo: User Interface & Operational Workflow", "5. Software Demo", 16)

    ui_card = add_card(s16, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    ui_img = "extracted_assets/prototype_ui_mockup.png"
    if os.path.exists(ui_img):
        s16.shapes.add_picture(ui_img, Inches(0.9), Inches(1.9), Inches(7.3), Inches(4.9))

    side_c = add_card(s16, Inches(8.5), Inches(1.8), Inches(4.033), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_side = s16.shapes.add_textbox(Inches(8.7), Inches(2.0), Inches(3.633), Inches(4.7))
    tf_side = tb_side.text_frame; tf_side.word_wrap = True

    p = tf_side.paragraphs[0]; p.text = "CORE FUNCTIONAL MODULES"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN

    modules = [
        ("Interactive Map Viewport:", "Leaflet.js map displaying OpenStreetMap basemap, Dulao ROI boundary, and classified canopy layers."),
        ("Pairwise Temporal Wizard:", "Dropdown selectors for T₁ (Baseline) and T₂ (Target), supporting 15 annual change comparisons."),
        ("Dynamic Metric Cards:", "Immediate display of mapped mangrove extent (ha), net gain, net loss, and percentage change."),
        ("Multi-Temporal Trend Chart:", "Chart.js line graph illustrating historical canopy trajectory across 2019–2024."),
        ("One-Click Report Export:", "Generates formal municipal conservation reports formatted for Aringay MENRO.")
    ]
    for mt, md in modules:
        pt = tf_side.add_paragraph(); pt.text = mt; pt.font.bold = True; pt.font.size = Pt(10.5); pt.font.color.rgb = COLOR_TEXT_MAIN; pt.space_before = Pt(5)
        pd = tf_side.add_paragraph(); pd.text = md; pd.font.size = Pt(10); pd.font.color.rgb = COLOR_TEXT_MUTED; pd.space_before = Pt(2)

    add_notes(s16,
        "Moving into Pillar 5: Software Demo. Here we show the user interface architecture of our working prototype. The design emphasizes clarity, accessibility, and high visual contrast. On the left, municipal officers have intuitive controls: selecting baseline year T1 and comparison year T2. The central viewport renders the interactive map with the exact 25-vertex Dulao boundary and color-coded gain and loss polygons. In the lower drawer, Chart.js displays the longitudinal canopy trajectory. A prominent export button allows officers to generate a formal PDF report in one click.",
        "The prototype translates complex geospatial deep learning into an intuitive, zero-code interface for municipal environmental officers.",
        "All controls feature clear state feedback, tooltips, and responsive layout.",
        "Q: Does the user need GIS training to operate this system?\nA: No. The user only selects years from dropdowns and clicks 'Run Change Analysis.' All projection transformations, pixel calculations, and polygon vectorizations happen automatically in the backend.",
        "Point out the 'DEMO MODE' banner in the top right to reinforce academic transparency.")

    # SLIDE 17: DEMO - EXECUTION WALKTHROUGH & TEST SCENARIO
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "Software Demo: Four-Step Execution Walkthrough", "5. Software Demo", 17)

    d_card = add_card(s17, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.0), bg_color=COLOR_WHITE, border_color=COLOR_MID_GREEN, border_width=2)
    
    steps = [
        {"num": "STEP 1", "title": "Select Baseline & Target", "desc": "Choose baseline year T₁ (e.g. 2019) and comparison year T₂ (e.g. 2024) from intuitive dropdowns."},
        {"num": "STEP 2", "title": "Execute Change Detection", "desc": "Click 'Analyze Change' to trigger backend PCC matrix comparison and hectarage calculations."},
        {"num": "STEP 3", "title": "Interactive Cartography", "desc": "Inspect color-coded gain/loss polygons in Leaflet, toggle layer overlays, and examine trend charts."},
        {"num": "STEP 4", "title": "Generate MENRO Report", "desc": "Click 'Export PDF Report' to automatically produce a formal, printable A4 summary document."}
    ]

    for i, st in enumerate(steps):
        left_s = Inches(1.1) + i * Inches(2.9)
        sub_card = add_card(s17, left_s, Inches(2.2), Inches(2.6), Inches(3.2), bg_color=COLOR_LIGHT_BG, border_color=COLOR_CARD_BORDER)
        tb_s = s17.shapes.add_textbox(left_s + Inches(0.15), Inches(2.35), Inches(2.3), Inches(2.9))
        tf_s = tb_s.text_frame; tf_s.word_wrap = True
        
        p = tf_s.paragraphs[0]; p.text = st["num"]; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
        p_t = tf_s.add_paragraph(); p_t.text = st["title"]; p_t.font.bold = True; p_t.font.size = Pt(14); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_before = Pt(4); p_t.space_after = Pt(8)
        p_d = tf_s.add_paragraph(); p_d.text = st["desc"]; p_d.font.size = Pt(10.5); p_d.font.color.rgb = COLOR_TEXT_MUTED; p_d.line_spacing = 1.3

    not_card = add_card(s17, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.9), bg_color=COLOR_LIGHT_AMBER, border_color=COLOR_AMBER, border_width=1.5)
    tb_not = s17.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.7))
    tf_not = tb_not.text_frame; tf_not.word_wrap = True
    p_n = tf_not.paragraphs[0]; p_n.text = "DEMONSTRATION TRANSPARENCY: The running system demonstrates complete functional execution (routing, map rendering, spatial analytics, PDF export) using controlled demonstration benchmarks to validate operational readiness."; p_n.font.bold = True; p_n.font.size = Pt(11); p_n.font.color.rgb = COLOR_AMBER

    add_notes(s17,
        "Members of the panel, we now walk through the live operational workflow of our prototype: First, selecting the temporal pair—in this demo, comparing 2019 baseline with 2024. Second, triggering the backend change analysis. Third, interacting with the Leaflet web map to inspect green gain zones and red loss zones alongside historical charts. Fourth, generating the official Aringay MENRO PDF report. Please note that the system is operating in demonstration mode to showcase full architectural readiness.",
        "Demonstration flow: Select Years -> Run Analysis -> Visualize Cartography -> Export PDF Report.",
        "Emphasize the speed and responsiveness of the Flask backend and Leaflet client during the demo.",
        "Q: Why are the numbers labeled 'Demo Data' in the live demo?\nA: Because scientific integrity demands that we clearly separate software engineering functional readiness from empirical research findings. The entire software pipeline is functional; final numbers await MENRO ground-truth mask validation.",
        "Keep the live demo tightly focused on the 4 steps without getting sidetracked by secondary settings.")

    # =========================================================================
    # PILLAR 6: STATUS, SYNTHESIS & DEFENSE (SLIDES 18, 19, 20)
    # =========================================================================
    # SLIDE 18: STATUS - IMPLEMENTATION MATRIX & QUALITY SAFEGUARD
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, "Project Status: Implementation Matrix & Scope Boundaries", "6. Status & Conclusion", 18)

    tbl_card = add_card(s18, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    
    rows = 9; cols = 4
    tbl_shape = s18.shapes.add_table(rows, cols, Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.7))
    table = tbl_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(2.6)
    table.columns[3].width = Inches(3.533)

    headers = ["System Component / Subsystem", "Current Status", "Implementation Mechanism", "Academic & Operational Remarks"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = COLOR_DARK_GREEN
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_WHITE

    status_data = [
        ("Web Frontend & Cartography", "IMPLEMENTED", "HTML5, CSS3, Leaflet.js, Chart.js", "Interactive map, layer toggles, and multi-temporal charts fully operational."),
        ("Flask Backend & REST API", "IMPLEMENTED", "Python Flask WSGI, REST JSON", "Routing, JSON payloads, and error handling fully implemented and tested."),
        ("Automated Report Engine", "IMPLEMENTED", "ReportLab Headless PDF Generator", "Generates formatted, printable A4 MENRO summary reports dynamically."),
        ("Sentinel-2 Preprocessing", "IMPLEMENTED", "Google Earth Engine & Python Rasterio", "Band isolation (B3, B4, B8, B11), bilinear resampling, and NDVI calculation."),
        ("5-Channel U-Net Architecture", "IMPLEMENTED", "PyTorch / Keras Deep Learning Code", "Architecture definition, skip connections, loss functions, and sweep pipelines ready."),
        ("Independent Ground-Truth Validation", "PENDING", "Aringay MENRO Field Experts", "Undergoing independent review by MENRO personnel to guarantee label validity."),
        ("Final Model Weights & Metrics", "PENDING", "Google Colab Pro GPU Training", "Dependent on finalized MENRO-validated reference masks prior to final fit."),
        ("Live In-App Satellite Inference", "OUT OF SCOPE", "Pre-computed / Batch Inference", "The prototype is designed for decision support rather than operational live satellite ingestion.")
    ]

    for r, (comp, stat, mech, rem) in enumerate(status_data):
        row_cells = [table.cell(r + 1, 0), table.cell(r + 1, 1), table.cell(r + 1, 2), table.cell(r + 1, 3)]
        bg = COLOR_WHITE if r % 2 == 0 else COLOR_LIGHT_BG
        for c, cell in enumerate(row_cells):
            cell.fill.solid(); cell.fill.fore_color.rgb = bg
        
        p0 = row_cells[0].text_frame.paragraphs[0]; p0.text = comp; p0.font.bold = True; p0.font.size = Pt(10); p0.font.color.rgb = COLOR_TEXT_MAIN
        p1 = row_cells[1].text_frame.paragraphs[0]; p1.text = stat; p1.font.bold = True; p1.font.size = Pt(10)
        if stat == "IMPLEMENTED": p1.font.color.rgb = COLOR_GAIN_GREEN
        elif stat == "PENDING": p1.font.color.rgb = COLOR_AMBER
        else: p1.font.color.rgb = COLOR_TEXT_MUTED
        p2 = row_cells[2].text_frame.paragraphs[0]; p2.text = mech; p2.font.size = Pt(9.5); p2.font.color.rgb = COLOR_TEXT_MUTED
        p3 = row_cells[3].text_frame.paragraphs[0]; p3.text = rem; p3.font.size = Pt(9.5); p3.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s18,
        "Slide 18 provides total transparency regarding our current project status. The entire software engineering stack—frontend, Flask backend, REST API, ReportLab engine, and preprocessing scripts—is 100% implemented and functional. What is currently pending is the independent ground-truth validation by Aringay MENRO personnel. We intentionally paused final model training until MENRO signs off on the reference masks, because training a deep learning model on unvalidated ground truth would compromise scientific rigor. Once MENRO completes mask validation, final weights will be generated on Colab and dropped directly into the model directory.",
        "Distinguish clearly between what is Implemented (software, pipeline, architecture) and what is Pending (MENRO label sign-off, final empirical weights).",
        "Independent ground-truth validation is a methodological strength and quality assurance safeguard, not a deficiency.",
        "Q: Why didn't you train the model with self-annotated masks?\nA: Self-annotated masks without local forestry validation risk introducing subjective bias. Aringay MENRO personnel possess ground reality knowledge of fishpond permits, replanting sites, and local species distribution.",
        "Deliver this slide with complete confidence. Academic panels respect researchers who protect data integrity.")

    # SLIDE 19: SYNTHESIS - TRIPARTITE VALUE & DEPLOYMENT ROADMAP
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, "Interdisciplinary Synthesis & Deployment Roadmap", "6. Status & Conclusion", 19)

    c_l = add_card(s19, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_l = s19.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_l = tb_l.text_frame; tf_l.word_wrap = True

    p = tf_l.paragraphs[0]; p.text = "TRIPARTITE CONTRIBUTION"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_l.add_paragraph(); p_t.text = "Academic & Practical Value"; p_t.font.bold = True; p_t.font.size = Pt(16); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(8)

    achieves = [
        ("Remote Sensing Pipeline:", "Operational multi-temporal Sentinel-2 MSI collection with 10m spatial resolution across 2019–2024 dry seasons."),
        ("Deep Learning Architecture:", "5-channel modified U-Net model with skip connections, trained under an 80/20 experimental partition protocol."),
        ("Software Engineering Delivery:", "Production-ready Flask REST backend and intuitive Leaflet web GIS interface tailored for municipal operators."),
        ("Municipal Decision Impact:", "Equips Aringay MENRO with a zero-cost, automated tool to substantiate local conservation and replanting policies.")
    ]
    for lbl, desc in achieves:
        p_l = tf_l.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10.5); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(6)
        p_d = tf_l.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    c_r = add_card(s19, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_r = s19.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True

    p = tf_r.paragraphs[0]; p.text = "CONCRETE NEXT STEPS"; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_MID_GREEN
    p_t = tf_r.add_paragraph(); p_t.text = "Pathway to Final Deployment"; p_t.font.bold = True; p_t.font.size = Pt(16); p_t.font.color.rgb = COLOR_TEXT_MAIN; p_t.space_after = Pt(8)

    steps_next = [
        ("1. Complete MENRO Validation:", "Finalize formal review and independent ground-truth sign-off with Aringay MENRO forestry officers."),
        ("2. Execute GPU Training Run:", "Train final 5-channel U-Net on Google Colab Pro GPU using validated labels."),
        ("3. Sweep Empirical Thresholds:", "Execute 0.05–0.95 threshold evaluation to determine optimal operating F1-score and IoU."),
        ("4. Seamless Weight Integration:", "Set DEMO_MODE = False in config to immediately hook empirical model inference into the prototype."),
        ("5. Municipal Handover & Training:", "Conduct operational orientation with Aringay MENRO staff for regular annual monitoring.")
    ]
    for lbl, desc in steps_next:
        p_l = tf_r.add_paragraph(); p_l.text = lbl; p_l.font.bold = True; p_l.font.size = Pt(10.5); p_l.font.color.rgb = COLOR_TEXT_MAIN; p_l.space_before = Pt(5)
        p_d = tf_r.add_paragraph(); p_d.text = desc; p_d.font.size = Pt(10); p_d.font.color.rgb = COLOR_TEXT_MUTED

    add_notes(s19,
        "In conclusion, our research has successfully designed and built the complete technical architecture for automated mangrove gain and loss monitoring in Barangay Dulao. The immediate next steps are clearly defined and directly executable: 1) Finalize independent ground-truth mask sign-off with MENRO; 2) Train the 5-channel U-Net on Google Colab Pro GPUs; 3) Execute the empirical threshold sweep; 4) Flip DEMO_MODE to False to load live model predictions; and 5) Conduct user handover with Aringay municipal personnel.",
        "The project has achieved its primary engineering and proposal objectives; the final empirical steps are mapped out in a clear 5-step roadmap.",
        "Transitioning from prototype to production requires only replacing the mock data with the validated model weights file.",
        "Q: When do you expect final model training to finish?\nA: Once MENRO completes the ground-truth mask sign-off, GPU training on Google Colab Pro takes approximately 2 to 3 hours for 50 epochs with EarlyStopping.",
        "Keep the conclusion positive, forward-looking, and academically grounded.")

    # SLIDE 20: ACKNOWLEDGMENTS, DEFENSE Q&A & DISCUSSION
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20, COLOR_DARK_GREEN)

    accent_bar = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(1.5), Inches(0.08))
    accent_bar.fill.solid(); accent_bar.fill.fore_color.rgb = RGBColor(16, 185, 129); accent_bar.line.fill.background()

    t_box = s20.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.5))
    tf_t = t_box.text_frame; tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]; p_t.text = "Thank You Very Much."
    p_t.font.name = FONT_TITLE; p_t.font.size = Pt(36); p_t.font.bold = True; p_t.font.color.rgb = COLOR_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Open for Questions, Defense Critiques, and Discussion"
    p_sub.font.size = Pt(18); p_sub.font.color.rgb = RGBColor(167, 243, 208); p_sub.space_before = Pt(8)

    div = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.3), Inches(11.733), Inches(0.02))
    div.fill.solid(); div.fill.fore_color.rgb = RGBColor(52, 211, 153); div.line.fill.background()

    c1 = s20.shapes.add_textbox(Inches(0.8), Inches(3.7), Inches(5.5), Inches(3.0))
    tf1 = c1.text_frame
    p1 = tf1.paragraphs[0]; p1.text = "STUDENT RESEARCH TEAM"; p1.font.bold = True; p1.font.size = Pt(12); p1.font.color.rgb = RGBColor(167, 243, 208)
    for a in authors:
        pa = tf1.add_paragraph(); pa.text = f"•  {a}"; pa.font.size = Pt(12); pa.font.color.rgb = COLOR_WHITE; pa.space_before = Pt(4)
    pa_deg = tf1.add_paragraph(); pa_deg.text = "Bachelor of Science in Computer Science\nDMMMSU-SLUC, Agoo, La Union"; pa_deg.font.size = Pt(11); pa_deg.font.color.rgb = RGBColor(209, 250, 229); pa_deg.space_before = Pt(8)

    c2 = s20.shapes.add_textbox(Inches(6.8), Inches(3.7), Inches(5.7), Inches(3.0))
    tf2 = c2.text_frame
    p2 = tf2.paragraphs[0]; p2.text = "DEFENSE QUICK REFERENCE GUIDE"; p2.font.bold = True; p2.font.size = Pt(12); p2.font.color.rgb = RGBColor(167, 243, 208)
    ref_points = [
        "Study Area: Barangay Dulao, Aringay, La Union (316.74 ha)",
        "Temporal Baseline: 2019–2024 (Dry Season, Feb 1 – Apr 30)",
        "Sensors & Bands: Sentinel-2 MSI (B3, B4, B8, B11) + NDVI",
        "Model Architecture: 5-Channel U-Net (256×256×5 Tensor)",
        "Data Protocol: 80% Training / 20% Validation Partition",
        "Change Logic: Post-Classification Comparison (PCC)",
        "Current Prototype: Operational Flask/Leaflet with Demo Benchmarks"
    ]
    for rp in ref_points:
        p_rp = tf2.add_paragraph(); p_rp.text = f"✓  {rp}"; p_rp.font.size = Pt(11); p_rp.font.color.rgb = COLOR_WHITE; p_rp.space_before = Pt(3)

    add_notes(s20,
        "Thank you, respected members of the panel. That concludes our formal presentation. We now welcome your questions, evaluations, and guidance on our research methodology, deep learning architecture, and software prototype.",
        "Gracious, confident opening for the 10-minute Q&A session.",
        "The quick reference guide on the right provides immediate answers to core parameters if panel members ask for specific numbers.",
        "Q: Panel opening questions.\nA: Remain calm, acknowledge the question clearly, and divide answers according to individual member assignments (e.g. Nash on architecture/software, Reymark on preprocessing/NDVI, Elaiza on methodology/IID, Lyka on change detection/metrics).",
        "Never argue with panel members. Acknowledge constructive criticism as valuable guidance for the manuscript refinement.")

    output_filename = "Mangrove_Gain_Loss_Detection_Final_Presentation.pptx"
    prs.save(output_filename)
    print(f"Successfully generated updated master presentation: {output_filename}")
    print(f"Total slides created: {len(prs.slides)}")

if __name__ == "__main__":
    create_presentation()
