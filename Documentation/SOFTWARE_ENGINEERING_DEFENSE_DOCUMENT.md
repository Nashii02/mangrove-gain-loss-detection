# Software Engineering Defense & Technical Reference Document

**Project Title:** Deep Learning-Based Detection of Mangrove Gain and Loss in Barangay Dulao, Aringay, La Union Using U-Net and Sentinel-2 Imagery  
**Academic Degree:** Bachelor of Science in Computer Science (BSCS)  
**Academic Institution:** Don Mariano Marcos Memorial State University, South La Union Campus (DMMMSU-SLUC), College of Computer Science, Agoo, La Union  
**Student Researchers:**
- Nash Francis M. Caluza
- Reymark O. Boado
- Elaiza Praise Y. Milana
- Lyka B. Vejano  
**Thesis Adviser:** Dr. Fernan H. Mendoza  
**Partner Agency / Primary Stakeholder:** Municipal Environment and Natural Resources Office (MENRO), Aringay, La Union  
**Academic Course:** Software Engineering 2  

---

## Executive Summary & Document Purpose

This document serves as the formal **Software Engineering Defense Manual and Technical Specification** for the thesis project. It is structured into the five core software engineering defense dimensions:
1. **[Section 1: Project Overview](#1-project-overview)**
2. **[Section 2: Project Scope](#2-project-scope)**
3. **[Section 3: Software Development Methodology](#3-software-development-methodology)**
4. **[Section 4: Software Requirements and System Models](#4-software-requirements-and-system-models)**
5. **[Section 5: Software Demo & Operational Walkthrough](#5-software-demo--operational-walkthrough)**
6. **[Section 6: Implementation Status, Quality Assurance & Defense Q&A](#6-implementation-status-quality-assurance--defense-qa)**

---

# 1. Project Overview

### 1.1 Ecological Context & Motivation
Mangroves are ecologically irreplaceable intertidal forest ecosystems that provide vital ecosystem services across Philippine coastal communities:
- **Storm Surge & Wave Attenuation:** Dense stilt root systems and trunk complexes dissipate wave energy by up to 66% over 100 meters of forest width, buffering coastal communities against typhoons.
- **Blue Carbon Sequestration:** Mangrove soils sequester carbon at rates up to four times higher per hectare than terrestrial tropical rainforests.
- **Estuarine Nursery Grounds:** Crucial breeding habitats for commercial fish, shrimp, mud crabs, and coastal mollusks.

Despite these critical functions, coastal mangrove cover in Barangay Dulao, Aringay, La Union has experienced ongoing anthropomorphic and natural stresses, including:
1. Conversion of intertidal wetlands into brackish aquaculture fishponds.
2. Unplanned coastal infrastructure and residential encroachment along riverbanks.
3. Severe hydrodynamic scouring and root exposure from seasonal typhoons along Lingayen Gulf.

### 1.2 The Problem Statement
Local environmental administrators—specifically the **Municipal Environment and Natural Resources Office (MENRO) of Aringay**—face three fundamental monitoring bottlenecks:
1. **Spatial Inaccessibility & Safety Hazards:** The 316.74-hectare mangrove zone along the Aringay River mouth features deep, muddy intertidal soils, dense stilt roots, and tidal fluctuations. Exhaustive ground surveys on foot are physically dangerous and cost-prohibitive.
2. **Spectral Confusion in Traditional Remote Sensing:** Conventional vegetation mapping relies on simple pixel-based thresholding (e.g., standard NDVI cutoffs). These methods routinely confuse mangrove canopies with terrestrial farmland, roadside trees, and fishpond surface algae.
3. **The Software Usability Gap:** Academic remote sensing outputs are typically delivered as complex GIS shapefiles or raw command-line scripts. Municipal officers lack specialized GIS workstations or programming backgrounds, preventing academic models from influencing real-time environmental enforcement.

### 1.3 General Objective
To develop an automated, web-based decision-support system for detecting and quantifying mangrove canopy gain and loss in Barangay Dulao, Aringay, La Union from 2019 to 2024 by integrating multi-spectral Sentinel-2 satellite imagery, a 5-channel U-Net deep convolutional neural network, and an interactive Flask/Leaflet web GIS prototype.

### 1.4 Specific Objectives
- **Specific Objective 1 (Data & Preprocessing Pipeline):** Acquire Copernicus Sentinel-2 Level-2A surface reflectance scenes for Barangay Dulao across the 2019–2024 dry seasons; extract Green (B3), Red (B4), Near-Infrared (B8), and Short-Wave Infrared (B11); bilinearly resample Band 11 to 10-meter resolution; calculate normalized NDVI; and construct standardized 5-channel $256 \times 256$ input tensors.
- **Specific Objective 2 (Deep Learning Segmentation & Evaluation):** Design and train a modified 5-channel U-Net semantic segmentation network using an 80/20 train-validation protocol, Adam optimization, Binary Cross-Entropy loss, and EarlyStopping; evaluate performance using Precision, Recall, F1-score, Intersection over Union (IoU), and mAP across a 0.05–0.95 classification threshold sweep.
- **Specific Objective 3 (Post-Classification Comparison & Web Prototype):** Implement a Post-Classification Comparison (PCC) transition matrix algorithm to map Gain, Loss, Stable Mangrove, and Stable Non-mangrove across all 15 pairwise annual epochs; build a responsive three-tier web application using Flask, Leaflet.js, and Chart.js; and incorporate automated one-click A4 PDF reporting for Aringay MENRO.

---

# 2. Project Scope

### 2.1 Geographic Delimitation (Study Area)
- **Target Site:** Barangay Dulao, Municipality of Aringay, Province of La Union, Region I, Philippines.
- **Authoritative Polygon:** Defined by an official 25-vertex Region of Interest (ROI) polygon matching `Data_&_Schema/samples/studu_area_boundary.geojson` and `Source_Code/preprocessing/config.py`.
- **Authoritative Study Area Envelope:** **Exactly 316.74 Hectares**.
- **Geographic Coordinates (EPSG:4326):**
  - Longitude Range: $120.320317^\circ\text{E}$ to $120.342991^\circ\text{E}$
  - Latitude Range: $16.363873^\circ\text{N}$ to $16.387870^\circ\text{N}$

### 2.2 Temporal Baseline & Seasonal Window
- **Observation Years:** Six discrete annual epochs: **2019, 2020, 2021, 2022, 2023, and 2024**.
- **Seasonal Window:** Strictly delimited to **February 1 to April 30 (Dry Season)**.
- **Atmospheric Filter:** Only satellite scenes with **Scene Cloud Cover < 20%** are admitted to prevent cloud shadow masking and monsoonal haze.

### 2.3 Functional In-Scope Capabilities
| Functional Capability | Description | Verification in Prototype |
|---|---|---|
| **Multi-Spectral Ingestion** | Reads Level-2A surface reflectance for Bands B3, B4, B8, and B11 | Automated in `preprocessing/pipeline.py` |
| **Bilinear Resampling** | Upsamples B11 from native 20m to 10m spatial grid | Rasterio / GDAL bilinear interpolation |
| **NDVI Computation** | Calculates Normalized Difference Vegetation Index and normalizes to $[0, 1]$ | Formula: `(B8 - B4) / (B8 + B4)` |
| **Deep Learning Segmentation** | 5-channel modified U-Net classifies binary canopy cover | Evaluated across 0.05–0.95 threshold sweep |
| **Pairwise Change Engine** | Evaluates all 15 permutations of $(T_1, T_2)$ where $T_1 < T_2$ | `/api/change-detection?from={T1}&to={T2}` |
| **Cartographic Web Interface** | Interactive Leaflet map with vector overlays and layer toggles | Responsive HTML5/CSS3/JavaScript client |
| **Statistical Analytics** | Mapped area calculation (ha), net change, and Chart.js trends | Computed on backend and rendered via Chart.js |
| **Automated PDF Export** | Generates formal, printable A4 conservation summary report | Headless ReportLab engine in `report_generator.py` |

### 2.4 Out-of-Scope & System Delimitations
To ensure operational focus and engineering feasibility, the following boundaries are established:
1. **Live In-App Satellite Ingestion:** The web application is engineered for decision support and planning rather than real-time orbital telemetry ingestion. Satellite composites are pre-processed offline to guarantee instantaneous dashboard response times.
2. **Species-Level Taxonomic Distinction:** The system performs binary canopy classification (Mangrove vs. Non-Mangrove). Differentiating *Rhizophora apiculata* from *Avicennia marina* requires sub-meter drone LiDAR or hyperspectral imagery beyond Sentinel-2's 10m ground resolution.
3. **Monsoonal / Wet Season Observation:** The rainy season (May through January) is excluded because chronic tropical cloud cover exceeds 70–80%, rendering optical multi-spectral sensors ineffective.
4. **Commercial Satellite Imagery:** Expensive proprietary satellites (Maxar, PlanetScope) are excluded to ensure zero recurring licensing fees for local government budgets.

---

# 3. Software Development Methodology

### 3.1 The Iterative & Incremental Development (IID) Model
The system was engineered using the **Iterative and Incremental Development (IID)** model (Larman & Basili, 2003; adapted from Ibrahim et al., 2011), as documented in Figure 1 of the thesis manuscript (page 11).

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 1: Domain Analysis & Requirements (MENRO Consultation)   │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 2: Satellite Acquisition (GEE Dry-Season Scenes)         │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 3: Preprocessing, Harmonization & 5D Tensor Stack        │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 4: Dataset Preparation & 80/20 Partition Protocol        │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 5: 5-Channel U-Net Architecture Construction             │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 6: Model Training, EarlyStopping & Threshold Sweep       │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 7: Post-Classification Comparison (PCC) Engine           │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Phase 8: Flask REST Web Prototype & Automated PDF Reports      │
   └────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Technology Stack Justification
- **Backend Framework (Python Flask WSGI):** Chosen for its minimalist footprint, direct interoperability with geospatial C-libraries (GDAL, Rasterio, Shapely), and seamless execution of scientific NumPy arrays and deep learning runtimes without the overhead of enterprise frameworks like Django.
- **Frontend Presentation (Vanilla HTML5 / Modern CSS / Vanilla JS):** Avoids heavy frontend build tooling (Node.js/Webpack/Vite), allowing the application to be deployed directly from Python with zero compilation steps.
- **Cartographic Engine (Leaflet.js 1.9):** High-performance, open-source mobile-friendly web mapping library that renders GeoJSON vector layers and OpenStreetMap basemap tiles smoothly on commodity municipal hardware.
- **Visualization Library (Chart.js 4.4):** Lightweight canvas-based charting library that renders multi-temporal canopy trajectories without DOM overhead.
- **Document Generation (ReportLab 5.0):** Enterprise-grade headless PDF generator that dynamically builds vector-crisp, printable A4 reports directly in memory.

### 3.3 Data Partitioning & Experimental Protocol
- **80% Training Partition:** Allocated to backpropagation weight updates via the Adam optimizer ($lr=0.001$).
- **20% Validation Partition:** Completely isolated holdout set evaluated at the end of each training epoch.
- **Academic Integrity Verification:** The 80/20 data partition is our **study-specific experimental protocol**. It is NOT cited or attributed to external papers.
- **Loss Function:** Binary Cross-Entropy (BCE):
  $$\mathcal{L}_{\text{BCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
- **Regularization:** `EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)`.

### 3.4 Quality Assurance & Testing Protocol
The codebase implements automated software verification assertions:
1. **Mathematical Partition Invariance:**
   $$\text{Area}_{\text{ROI}} = \text{Area}_{\text{Gain}} + \text{Area}_{\text{Loss}} + \text{Area}_{\text{Stable Mangrove}} + \text{Area}_{\text{Stable Non-Mangrove}} = 316.74\text{ ha}$$
2. **Spatial Clamping Tests:** GeoJSON coordinates are checked against the bounding box $[120.320^\circ\text{E}, 16.364^\circ\text{N}, 120.343^\circ\text{E}, 16.388^\circ\text{N}]$ to prevent coordinate drift.
3. **API Contract Verification:** Endpoints validate input parameter types; non-existent year requests return HTTP 400 with descriptive JSON error payloads.
4. **Binary PDF Stream Integrity:** Generated PDF buffers are validated for valid PDF byte signatures (`%PDF-1.4`) and non-empty byte arrays.

---

# 4. Software Requirements and System Models

### 4.1 Functional Requirements Specification
- **FR-01 (Spatial ROI Loading):** The system shall load and render the authoritative 25-point polygon boundary of Barangay Dulao (316.74 ha) upon application initialization.
- **FR-02 (Pairwise Temporal Analysis):** The system shall allow users to select any two distinct years $T_1$ and $T_2$ ($2019 \le T_1 < T_2 \le 2024$) and compute the net canopy change.
- **FR-03 (Four-Class Classification):** The system shall categorize every pixel inside the ROI into one of four thematic classes: Gain (+1), Loss (-1), Stable Mangrove (2), or Stable Non-Mangrove (0).
- **FR-04 (Statistical Metrics Computation):** The system shall calculate total mangrove extent in hectares for each year, net hectarage gain, net hectarage loss, and percentage change.
- **FR-05 (Dynamic Cartography):** The system shall render interactive map layers with individual toggle controls for Gain (Green), Loss (Red), Stable (Dark Green), and ROI boundary (Outline).
- **FR-06 (Automated PDF Reporting):** The system shall generate a formatted A4 PDF summary document containing municipality branding, spatial summary tables, and formal planning disclaimers.

### 4.2 Non-Functional Requirements Specification
- **NFR-01 (Performance & Latency):** All REST API queries (`/api/change-detection`, `/api/statistics`) shall return responses within 2.0 seconds on standard local server execution.
- **NFR-02 (Usability & Accessibility):** The web user interface shall be zero-code, requiring no GIS software installation or command-line scripting by municipal personnel.
- **NFR-03 (Mathematical Consistency):** Pixel-based area tallies across all four classes must sum to exactly 316.74 ha ($\pm 0.01$ ha due to pixel quantization).
- **NFR-04 (Modularity & Maintainability):** The backend shall remain decoupled from the frontend through standardized JSON REST contracts, enabling the ML pipeline to be updated independently.

### 4.3 Use Case Modeling
```
                         MANGROVE MONITORING SYSTEM
               ┌────────────────────────────────────────────────────────┐
               │                                                        │
               │   (UC-1: Select Annual Baseline Epochs T₁ & T₂)        │
               │                       ▲                                │
               │                       │                                │
               │   (UC-2: Run Post-Classification Comparison)           │
               │                       ▲                                │
[MENRO User] ──┼───────────────────────┼────────────────────────────────┤── [Researcher]
               │                       │                                │
               │   (UC-3: Inspect Interactive Map & Layer Toggles)      │
               │                       ▲                                │
               │                       │                                │
               │   (UC-4: Analyze Multi-Temporal Extent Charts)         │
               │                       ▲                                │
               │                       │                                │
               │   (UC-5: Generate & Download Official A4 PDF Report)   │
               │                                                        │
               └────────────────────────────────────────────────────────┘
```

### 4.4 Three-Tier Architecture Model
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TIER 1: PRESENTATION LAYER                            │
│  - Responsive HTML5 & Semantic Layout                                       │
│  - Leaflet.js Interactive Web Map & Custom Canvas Vector Layer Renderers    │
│  - Chart.js Multi-Temporal Line Charts (2019–2024 Extent Trajectory)       │
│  - Dynamic DOM Metric Badges (Net Gain / Loss Hectarage)                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP GET (JSON REST API)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TIER 2: APPLICATION LAYER                           │
│  - Python Flask WSGI Web Application Server                                 │
│  - Route Controllers: `/`, `/api/study-area`, `/api/statistics`,           │
│                       `/api/change-detection`, `/report/download`           │
│  - Post-Classification Comparison (PCC) Transition Matrix Engine            │
│  - ReportLab Headless Document Generation Engine                            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Local File I/O & Memory Arrays
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      TIER 3: DATA & STORAGE LAYER                           │
│  - Sentinel-2 Level-2A Multi-Spectral Surface Reflectance (B3, B4, B8, B11)  │
│  - Derived NDVI Surface Arrays (Normalized [0, 1])                          │
│  - Authoritative Dulao 25-Point ROI GeoJSON (`dulao_mangrove_roi.geojson`)  │
│  - Model Artifacts (`models/final_model.keras` / Pre-computed Masks)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.5 The Multi-Spectral 5D Feature Tensor Model
$$\mathbf{X} \in \mathbb{R}^{256 \times 256 \times 5}$$
Where the five channels represent:
1. $\mathbf{X}_{:,:,0} = \text{Band 3 (Green, } 560\text{ nm, } 10\text{m resolution)}$
2. $\mathbf{X}_{:,:,1} = \text{Band 4 (Red, } 665\text{ nm, } 10\text{m resolution)}$
3. $\mathbf{X}_{:,:,2} = \text{Band 8 (Near-Infrared, } 842\text{ nm, } 10\text{m resolution)}$
4. $\mathbf{X}_{:,:,3} = \text{Band 11 (Short-Wave Infrared, } 1610\text{ nm, resampled to } 10\text{m)}$
5. $\mathbf{X}_{:,:,4} = \text{Normalized NDVI} = \frac{1}{2} \left[ \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}} + 1 \right]$

### 4.6 The 5-Channel U-Net Architecture Model
Adapted from Ronneberger et al. (2015), as documented in Figure 2 of the thesis proposal (page 15):
- **Contracting Path (Encoder):** 4 downsampling stages. Each stage contains two $3 \times 3$ convolutional layers (ReLU activation, He normal initialization) followed by a $2 \times 2$ max pooling layer with stride 2. Feature map channels double at each stage ($64 \to 128 \to 256 \to 512$).
- **Bottleneck Layer:** Deepest feature representations ($1024$ channels) capturing spatial context across the entire estuary.
- **Expansive Path (Decoder):** 4 upsampling stages. Each stage uses a $2 \times 2$ up-convolution (transposed convolution) that halves channel depth and doubles spatial resolution.
- **Skip Connections:** Concatenates high-resolution spatial feature maps directly from the contracting path to the corresponding expansive stage, preventing boundary fuzziness.
- **Output Layer:** $1 \times 1$ convolution with Sigmoid activation producing a single-channel probability map:
  $$\hat{Y}_{i,j} = \sigma(z_{i,j}) = \frac{1}{1 + e^{-z_{i,j}}} \in [0.0, 1.0]$$

### 4.7 Post-Classification Comparison (PCC) Mathematical Model
Given two classified binary masks $\mathbf{M}_{T_1}, \mathbf{M}_{T_2} \in \{0, 1\}^{H \times W}$ where $1 = \text{Mangrove}$ and $0 = \text{Non-Mangrove}$:
$$\mathbf{C}_{i,j} = \begin{cases}
+1 \text{ (Gain)}, & \text{if } \mathbf{M}_{T_1}(i,j) = 0 \text{ and } \mathbf{M}_{T_2}(i,j) = 1 \\
-1 \text{ (Loss)}, & \text{if } \mathbf{M}_{T_1}(i,j) = 1 \text{ and } \mathbf{M}_{T_2}(i,j) = 0 \\
+2 \text{ (Stable Mangrove)}, & \text{if } \mathbf{M}_{T_1}(i,j) = 1 \text{ and } \mathbf{M}_{T_2}(i,j) = 1 \\
0 \text{ (Stable Non-Mangrove)}, & \text{if } \mathbf{M}_{T_1}(i,j) = 0 \text{ and } \mathbf{M}_{T_2}(i,j) = 0
\end{cases}$$

Area quantification in hectares:
$$\text{Area}_{\text{Class}} = N_{\text{pixels}} \times 0.01\text{ ha}$$
(Since each $10\text{m} \times 10\text{m}$ pixel occupies exactly $100\text{ m}^2 = 0.01\text{ ha}$).

---

# 5. Software Demo & Operational Walkthrough

### 5.1 System Launch Procedure
1. **Prerequisites:** Python 3.10+ installed with dependencies listed in `Requirements.txt` (`Flask`, `reportlab`, `numpy`, `rasterio`).
2. **Execute Server:**
   ```bash
   cd Source_Code
   python app.py
   ```
3. **Open Client:** Navigate in any modern browser to `http://127.0.0.1:5000/`.

### 5.2 Step-by-Step Test Execution Script
During the final presentation, the presenter will execute the following four-step sequence:

- **Step 1: System Initialization & ROI Verification**
  - Verify that the header reads: *"Deep Learning-Based Detection of Mangrove Gain and Loss — Brgy. Dulao, Aringay, La Union"*.
  - Observe the red badge indicating **`DEMO MODE`**, demonstrating academic transparency.
  - Confirm the Leaflet map automatically centers on Barangay Dulao with the yellow 25-point ROI boundary line visible.

- **Step 2: Temporal Pair Selection**
  - Locate the **Temporal Analysis Controls** on the left sidebar.
  - Set Baseline Year ($T_1$) to **`2019`**.
  - Set Comparison Year ($T_2$) to **`2024`**.
  - Click the green button: **`Analyze Change`**.

- **Step 3: Cartographic & Metric Inspection**
  - Observe instantaneous update of the summary cards:
    - Mapped Extent $T_1$ (2019)
    - Mapped Extent $T_2$ (2024)
    - Net Detected Gain (+ ha)
    - Net Detected Loss (- ha)
  - Inspect the map viewport: green polygons indicate mangrove expansion/colonization; red polygons indicate cleared or eroded areas.
  - Review the bottom Chart.js trend line depicting the trajectory from 2019 to 2024.

- **Step 4: Formal PDF Report Generation**
  - Click the blue button: **`📄 Export MENRO PDF Report`**.
  - The browser immediately downloads `Aringay_MENRO_Mangrove_Report.pdf`.
  - Open the PDF to showcase the formal municipality header, spatial summary table, and planning disclaimers.

---

# 6. Implementation Status, Quality Assurance & Defense Q&A

### 6.1 Subsystem Implementation Matrix
| Subsystem Component | Engineering Status | Implementation Details | Academic / Operational Notes |
|---|---|---|---|
| **Web Frontend** | **IMPLEMENTED** | HTML5, CSS3, Leaflet.js, Chart.js | Operational dashboard, layer toggles, responsive layout |
| **Flask Backend & REST API** | **IMPLEMENTED** | Python Flask WSGI, JSON contracts | All 5 REST endpoints operational with error handling |
| **PDF Reporting Engine** | **IMPLEMENTED** | ReportLab Headless Engine | Generates formal A4 PDF reports dynamically |
| **Sentinel-2 Preprocessing** | **IMPLEMENTED** | Google Earth Engine & Rasterio | Band isolation, bilinear resampling, NDVI computation |
| **U-Net Architecture** | **IMPLEMENTED** | PyTorch / Keras Deep Learning | Symmetrical 5-channel model definition ready for training |
| **Independent Mask Validation** | **PENDING** | Aringay MENRO Forestry Personnel | Undergoing independent review to ensure label validity |
| **Final Model Weights & Metrics** | **PENDING** | Google Colab Pro GPU Training | Paused until MENRO mask sign-off to protect scientific rigor |
| **Live In-App Inference** | **OUT OF SCOPE** | Pre-computed Seasonal Composites | Decision support system; live orbital ingest is out of scope |

### 6.2 Anticipated Defense Q&A and Safe Academic Answers

**Q1: Why did you choose an 80/20 train-validation split instead of 70/30 or 5-fold cross-validation?**  
> *"The 80/20 partition was adopted by our research team as the study-specific experimental protocol. Given the spatial extent of the Dulao estuary, 80% provides adequate training volume for deep convolutional kernels while reserving an independent 20% holdout set to monitor generalization without spatial leakage."*  
> *(Caution: Never attribute the 80/20 split to Ronneberger or external authors).*

**Q2: What is your actual model accuracy right now?**  
> *"The metrics currently embedded in the prototype are controlled demonstration benchmarks used to validate software routing, statistical calculations, and PDF generation. Final empirical accuracy numbers (F1-score, IoU, mAP) will be computed once the independent MENRO ground-truth mask validation is finalized."*

**Q3: Why haven't you finalized model training yet?**  
> *"Our reference masks are currently undergoing independent ground-truth validation by Aringay MENRO forestry personnel. As a matter of scientific integrity, we intentionally paused final weight fitting until domain experts validate the ground-truth labels, ensuring our model is trained on ground reality rather than subjective self-annotation."*

**Q4: How does the software guarantee that area calculations are correct?**  
> *"Our software test suite verifies mathematical partition invariance: across all 15 pairwise comparisons, the sum of Gain, Loss, Stable Mangrove, and Stable Non-mangrove strictly equals the total 316.74-hectare area of the Dulao boundary without a single pixel omitted or duplicated."*

---
*Document verified and approved for submission to the Software Engineering 2 Examination Panel.*
