# 🌱 Mangrove Monitoring System

**Deep Learning-Based Detection of Mangrove Gain and Loss in Brgy. Dulao, Aringay, La Union**

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/framework-TensorFlow%20%2F%20Keras-orange)
![Model](https://img.shields.io/badge/model-U--Net-brightgreen)
![Data](https://img.shields.io/badge/data-Sentinel--2%20L2A-lightgrey)
![Period](https://img.shields.io/badge/period-2019--2024-informational)

An image processing system that will automatically detect and quantify mangrove cover change over time using Sentinel-2 satellite imagery and a U-Net deep learning segmentation model. Developed as an undergraduate thesis for the Aringay MENRO (Municipal Environment and Natural Resources Office) to support environmental monitoring and conservation planning.

---

## 👥 Team

| Member | Role |
|---|---|
| Caluza, Nash Francis M. | Researcher / Developer |
| Boado, Reymark O. | Researcher / Developer |
| Milana, Elaiza Praise Y. | Researcher / Developer |
| Vejano, Lyka B. | Researcher / Developer |
| Mendoza, Fernan H., DIT | Adviser |

**Bachelor of Science in Computer Science**
Don Mariano Marcos Memorial State University — South La Union Campus
College of Computer Science, Agoo, La Union · 2026

---
## 📋 Project Status

| Component | Status |
|---|---|
| Web prototype — frontend + REST API | ✅ Complete (running on demo data) |
| System design/Methodology | 🔄 Under revision |
| Pipeline scripts (preprocessing, training, evaluation) | 🔄 Under revision |
| Dataset acquisition (Sentinel-2, 2019–2024) | ⏳ Will be conducted after script finalization |
| Reference labeling + MENRO validation | ⏳ Planned |
| U-Net training & evaluation | ⏳ Planned |
| Multi-temporal change detection | ⏳ Planned |
| Full integration of real outputs | ⏳ Planned |

> The web application currently runs end-to-end on demo data so the interface, workflows, and API contracts can be reviewed while the machine learning pipeline is being finalized. All integration points are marked `>>> INTEGRATION` in `SourceCode/app.py`.

---

## 📌 Overview

Mangrove ecosystems protect coastal areas, support biodiversity, and maintain environmental balance — yet mangrove areas in the Philippines have declined considerably due to aquaculture expansion, land reclamation, and other land-use changes. No localized, automated mangrove monitoring scheme currently exists for Brgy. Dulao, Aringay, La Union.

This system addresses that gap by:

- Building a localized mangrove dataset from Sentinel-2 multispectral imagery
- Training a U-Net model for pixel-level binary semantic segmentation (mangrove vs. non-mangrove)
- Applying the locked model across 2019–2024 to produce annual mangrove maps
- Comparing consecutive years pixel-by-pixel to map mangrove gain and loss
- Quantifying transitions in hectares (10 m grid)
- Presenting results through a web prototype with maps, statistics, and a downloadable PDF report for the Aringay MENRO

---

## 🔁 Roadmap

- [x] Web frontend (Flask + Bootstrap 5 + Leaflet.js + Chart.js)
- [x] REST API with demo data
- [x] PDF report generation (ReportLab)
- [ ] Finalize and revise pipeline scripts
- [ ] Dataset acquisition — Sentinel-2 L2A via Google Earth Engine / Copernicus
- [ ] Image preprocessing — cloud masking, band alignment, NDVI, 256×256 patching
- [ ] Reference labeling — mangrove = 1 / non-mangrove = 0, validated by MENRO
- [ ] U-Net training (80/20 split) and evaluation (F1-score, IoU, mAP)
- [ ] Multi-temporal change detection (2019–2024, consecutive-year comparison)
- [ ] Integration of real model outputs into the web system

---

## 🛠️ Tech Stack

| Category | Tool | Purpose |
|---|---|---|
| Deep Learning | TensorFlow / Keras | U-Net model training & inference |
| Satellite imagery | Rasterio | Reading GeoTIFF / Sentinel-2 rasters |
| Data manipulation | NumPy | Band stacking, patching, change detection |
| Labels / shapefiles | GeoPandas | Mangrove masks & polygon handling |
| Visualization | Matplotlib | Development plots & quality checks |
| Training environment | Google Colab | Free GPU training |
| Web backend | Flask (Python) | Serves application + JSON API |
| Interactive maps | Leaflet.js | Displays GeoJSON layers |
| Statistics charts | Chart.js | Area statistics & evaluation charts |
| Frontend styling | Bootstrap 5 | Responsive UI |
| PDF reports | ReportLab | Downloadable reports for MENRO |
| Map layer format | GeoJSON / GeoTIFF | Standard geospatial formats |
| Satellite source | Copernicus / Google Earth Engine | Sentinel-2 L2A (free) |
| Label verification | QGIS | Reference label QC & correction |
| Version control | GitHub | Team coordination |
| Metrics | scikit-learn | IoU, F1, confusion matrix |

---

## 📂 Repository Structure

```
mangrove-monitoring-system/
├── SourceCode/                     Flask app, templates, static assets, ML pipeline
│   ├── app.py                      Backend: pages + REST API (demo data)
│   ├── templates/                  Dashboard, maps, statistics, evaluation, report
│   ├── static/                     CSS, JS (Leaflet maps, Chart.js)
│   └── preprocessing/              Pipeline scripts (to be added)
│
├── Documentation/                  Abstract, methodology, protocols, user manual
│
├── Dependencies and Environment/   requirements.txt, setup guide, Colab notebooks
│
├── Data and Schema/                File format specs, API schemas, sample data
│
└── Model/                          Model card, final metrics, weight storage notes
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or newer
- pip (or conda)
- For training (later): a Google Colab account with GPU runtime
- For data re-acquisition (later): a Google Earth Engine account

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/Nashii02/mangrove-monitoring-system.git
cd mangrove-monitoring-system

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r "Dependencies and Environment/requirements.txt"

# 4. Run the web prototype
cd SourceCode
python app.py
```

Open `http://127.0.0.1:5000` in your browser. The system runs on demo data; dataset acquisition, preprocessing, and training will be performed after the pipeline scripts are revised and finalized.

> Detailed setup (including Colab and Earth Engine authentication) is in `Dependencies and Environment/SETUP_GUIDE.md`.

---

## 🖥️ System Modules

| Module | Route | Description |
|---|---|---|
| Dashboard | `/` | Study area, observation period, model summary, workflow status |
| Annual Maps | `/maps` | Binary mangrove / non-mangrove map per year (2019–2024) |
| Change Detection | `/change` | Consecutive-year gain / loss maps with area summary |
| Statistics | `/statistics` | Cover-per-year chart, gain/loss chart, transition table |
| Model Evaluation | `/model` | F1-score, IoU, mAP, precision–recall curve, confusion matrix |
| Report | `/report` | Downloadable PDF summary (ReportLab) |

---

## 🔌 API Reference

| Endpoint | Method | Returns |
|---|---|---|
| `/api/meta` | GET | Years, study area, pixel size, model information |
| `/api/annual/<year>` | GET | GeoJSON of annual mangrove mask + area (ha) + pixel count |
| `/api/change/<y1>/<y2>` | GET | Consecutive-year gain/loss GeoJSON + area statistics |
| `/api/stats` | GET | Per-year cover and per-interval gain/loss (ha) |
| `/api/metrics` | GET | F1, IoU, mAP, threshold, PR curve, confusion matrix |
| `/api/report` | POST | Generated PDF (binary download) |

> All endpoints currently return demo data. Response schemas are documented in `Data and Schema/DATA_SCHEMA.md`.

---

## 🔄 Data Pipeline

*(planned — to be executed after script finalization)*

```
Sentinel-2 L2A imagery (2019–2024, same-season scenes)          — will be acquired
        │   bands: B3 (Green), B4 (Red), B8 (NIR), B11 (SWIR)
        │   NDVI = (B8 − B4) / (B8 + B4)
        ▼
Preprocessing                                                    — will be applied
        cloud/shadow masking (SCL) · 10 m grid alignment ·
        B11 bilinear resampling (20 m → 10 m) · normalization ·
        missing-pixel handling
        ▼
256 × 256 patches (5-channel input + patch index)                — will be generated
        ▼
Reference labeling (mangrove = 1, non-mangrove = 0)              — will be validated
        interpreted from reference datasets, local records,         by Aringay MENRO
        and high-resolution imagery; MENRO expert review
        ▼
U-Net training                                                   — will be trained
        80% train / 20% validation · Adam (lr = 0.001) ·
        binary cross-entropy loss
        ▼
Evaluation                                                       — will be assessed
        F1-score · IoU · mAP (threshold sweep 0.05–0.95) ·
        operating threshold = maximum validation IoU → locked
        ▼
Multi-temporal change detection                                  — will be run
        pixel-by-pixel consecutive-year comparison ·
        mapped gain / loss / stable areas in hectares
        ▼
Web prototype (Flask + Leaflet)                                  — READY
        annual maps · gain/loss maps · statistics · PDF report
```

---

## 🧮 Area Computation

The final classified imagery will use a **10-meter spatial grid**:

- 1 fully covered pixel = 100 m²
- **Area (ha) = N / 100**, where *N* is the number of classified pixels in the corresponding mangrove-cover category

**Transition categories** (consecutive-year comparison):

| Earlier Year | Later Year | Transition Category |
|---|---|---|
| Non-mangrove | Mangrove | Mapped mangrove gain |
| Mangrove | Non-mangrove | Mapped mangrove loss |
| Mangrove | Mangrove | Stable mangrove |
| Non-mangrove | Non-mangrove | Stable non-mangrove |

---

## 📊 Model Performance

*(to be reported after final training)*

| Metric | Result |
|---|---|
| F1-score | *to be reported* |
| Intersection over Union (IoU) | *to be reported* |
| mean Average Precision (mAP) | *to be reported* |
| Operating threshold (locked) | *to be reported* |

**Evaluation protocol:** pixel-level metrics with the mangrove class treated as the positive class; performance will be assessed against the first trained iteration as a baseline rather than a predetermined acceptance threshold. The final model configuration and classification threshold will be locked before application to the multi-temporal imagery.

> Final metrics will be published in `Model/MODEL_CARD.md` and served by `/api/metrics` after the final training run.

---

## ⚠️ Limitations & Interpretation Notes

- Detected transitions will be interpreted as **mapped land-cover changes, not confirmed ecological causes**. Possible causes (restoration, replanting, natural regeneration, erosion, harvesting, storm damage, tidal conditions, phenological differences, or classification errors) will only be discussed when supported by additional evidence.
- The study will not create a truly independent test dataset; validation results will be treated as estimates for the study's reference-data conditions.
- The 10 m spatial resolution may limit detection of very small or narrow mangrove fragments.

---

## 📖 Documentation

| Document | Contents |
|---|---|
| `Documentation/01_Abstract.md` | Study abstract |
| `Documentation/02_Methodology_Summary.md` | Research design & procedures |
| `Documentation/03_Data_Acquisition_Protocol.md` | Sentinel-2 retrieval & preprocessing |
| `Documentation/04_Labeling_Guidelines.md` | Mangrove identification rules + MENRO validation |
| `Documentation/05_User_Manual.md` | Operating the system (MENRO-facing) |
| `Data and Schema/DATA_SCHEMA.md` | File formats, API schemas, units & constants |
| `Model/MODEL_CARD.md` | Architecture, training configuration, metrics, limitations |

---


## 🙏 Acknowledgments

- **Aringay MENRO** — independent validation of reference labels
- **Copernicus / ESA** — freely available Sentinel-2 imagery
- **Google Earth Engine** — cloud-based processing platform

**Key references:** Ronneberger et al. (2015) — U-Net · Bunting et al. (2022) — Global Mangrove Watch v3.0 · Auxtero & Villamor (2026) — U-Net for Philippine mangrove mapping · Maung et al. (2024) · Jamaluddin & Chen (2024) · Xue & Qian (2022) — full list in the thesis manuscript.

---

*This prototype focuses on core functionality and output interpretability, not operationalization. Outputs will be presented to the Aringay MENRO.*
