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
| Vejano, Lyka B. | Researcher / Developer |

**Bachelor of Science in Computer Science**
Don Mariano Marcos Memorial State University — South La Union Campus
College of Computer Science, Agoo, La Union · 2026

---

## 📋 Project Status

This project is being built in two parallel tracks: a working web application (already functional), and the actual machine learning pipeline that will feed it real results (still in progress). We built it this way deliberately — the web interface can be reviewed, tested, and refined by our adviser and MENRO now, without waiting for the full dataset and trained model, which take much longer to produce.

| Component | Status |
|---|---|
| Web prototype — frontend + REST API | ✅ Complete (running on demo data) |
| System design / Methodology | 🔄 Under revision (post-proposal) |
| Pipeline scripts (preprocessing, training, evaluation) | 🔄 Under revision (v1 written, revision in progress) |
| Dataset acquisition (Sentinel-2, 2019–2024) | ⏳ Will be conducted after script finalization |
| Reference labeling + MENRO validation | ⏳ Planned |
| U-Net training & evaluation | ⏳ Planned |
| Multi-temporal change detection | ⏳ Planned |
| Full integration of real outputs | ⏳ Planned |

The web application currently runs end-to-end on demo data so the interface, workflows, and API contracts can be reviewed while the machine learning pipeline is being finalized. All integration points are marked `>>> INTEGRATION` in `SourceCode/app.py`.

Per-file ownership, version, and lifecycle status: see the Configuration Item Register & Tracking Log below.

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

In short: this repository contains everything needed to go from raw satellite imagery to a usable coastal-monitoring tool — the code, the data specifications, the trained model (once complete), and the documentation explaining how and why each part works.

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

Our tools split into two groups: one set for the machine learning side (training and evaluating the U-Net model), and another for the web application side (displaying results to MENRO). The table below also notes what each tool is actually used for, so the choice of each isn't just a name-drop.

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

The repository is organized so that the web application, machine learning pipeline, documentation, environment setup, data specifications, and model artifacts remain separated but connected. The structure below shows what each major folder and script is responsible for.

```
mangrove-gain-loss-detection/
├── SourceCode/
│   ├── app.py                     Main Flask application. Defines all web page
│   │                              routes (dashboard, maps, statistics, etc.) and
│   │                              REST API endpoints. This is the file you run to
│   │                              start the web prototype.
│   ├── templates/                 HTML pages rendered by Flask, one per module
│   │                              (dashboard, annual maps, change detection,
│   │                              statistics, model evaluation, report).
│   ├── static/                    Front-end assets: CSS for styling, and JS files
│   │                              that draw the interactive Leaflet maps and
│   │                              Chart.js graphs using data from the API.
│   └── preprocessing/             The actual machine learning pipeline — separate
│       ├── config.py              Central settings (file paths, band names, patch
│       │                          size, thresholds) so every script reads the same
│       │                          configuration instead of hardcoding values.
│       ├── gee_export.py          Connects to Google Earth Engine to search for and
│       │                          download Sentinel-2 L2A scenes for Barangay Dulao.
│       ├── make_patches.py        Cuts the downloaded imagery into 256×256 patches
│       │                          and stacks the 5 channels (B3, B4, B8, B11, NDVI).
│       ├── rasterize_labels.py    Converts hand-drawn/MENRO-validated mangrove
│       │                          boundaries (vector shapes) into the binary
│       │                          pixel masks (1 = mangrove, 0 = non-mangrove)
│       │                          used to train the model.
│       ├── unet_model.py          Defines the U-Net architecture itself — the
│       │                          encoder, bottleneck, decoder, and skip
│       │                          connections.
│       ├── train.py               Runs the actual training loop: loads patches,
│       │                          trains U-Net, saves the resulting model weights.
│       ├── evaluate.py            Loads a trained model and computes F1, IoU, and
│       │                          mAP on the validation set; also runs the
│       │                          threshold sweep to pick the locked threshold.
│       └── change_detection.py    Takes two years' finished segmentation maps and
│                                  produces the gain/loss/stable comparison.
│
├── Documentation/                 Human-readable explanations of the study and
│                                  system — not code.
│
├── Dependencies and Environment/  Everything needed to reproduce the exact software
│                                  environment (Python packages, Colab notebooks,
│                                  setup instructions) so any teammate — or your
│                                  adviser — can run the project identically.
│
├── Data and Schema/               Defines what the data actually looks like: file
│                                  formats, API response shapes, and small sample
│                                  files so a new developer can see real examples
│                                  without needing the full dataset.
│
└── Model/                         Everything about the trained model itself: its
                                   architecture card, its performance numbers, and
                                   where the actual weight files are stored.
```

**Status note:** pipeline scripts are at v1 (under revision) — descriptions above state each script's intended role in the finished workflow. Dataset acquisition, reference labeling, model training, and multi-temporal change detection will be executed after the revision round is complete (see Project Status and Data Pipeline below).

---

## 📋 Configuration Items (CI) Inventory

| Item ID | Item / File Name | Category | Filepath / Repository Path | Primary Owner | Current Version | Lifecycle Status |
|---|---|---|---|---|---|---|
| CI-01 | app.py | Source Code | /SourceCode/app.py | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-02 | templates/ (base, index, annual_maps, change_detection, statistics, model_evaluation, report) | Source Code | /SourceCode/templates/ | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-03 | style.css | Source Code | /SourceCode/static/css/style.css | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-04 | common.js, map_annual.js, map_change.js, charts.js | Source Code | /SourceCode/static/js/ | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-05 | config.py | Source Code | /SourceCode/preprocessing/config.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-06 | gee_export.py | Source Code | /SourceCode/preprocessing/gee_export.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-07 | make_patches.py | Source Code | /SourceCode/preprocessing/make_patches.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-08 | rasterize_labels.py | Source Code | /SourceCode/preprocessing/rasterize_labels.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-09 | unet_model.py | Source Code | /SourceCode/preprocessing/unet_model.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-10 | train.py | Source Code | /SourceCode/preprocessing/train.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-11 | evaluate.py | Source Code | /SourceCode/preprocessing/evaluate.py | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-12 | change_detection.py | Source Code | /SourceCode/preprocessing/change_detection.py | Nash Francis Caluza | v1.0 | 🔵 Reserved |
| CI-13 | preprocessing README.md | Source Code | /SourceCode/preprocessing/README.md | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-14 | README.md (root) | Documentation | /README.md | Lyka Vejano | v1.0 | 🟣 Revised (Post-Proposal) |
| CI-15 | 01_Abstract.md | Documentation | /Documentation/01_Abstract.md | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-16 | 02_Methodology_Summary.md | Documentation | /Documentation/02_Methodology_Summary.md | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-17 | 03_Data_Acquisition_Protocol.md | Documentation | /Documentation/03_Data_Acquisition_Protocol.md | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-18 | 04_Labeling_Guidelines.md | Documentation | /Documentation/04_Labeling_Guidelines.md | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-19 | 05_User_Manual.md | Documentation | /Documentation/05_User_Manual.md | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-20 | 06_Defense_Presentation.pdf | Documentation | /Documentation/06_Defense_Presentation.pdf | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-21 | 07_Thesis_Manuscript.pdf | Documentation | /Documentation/07_Thesis_Manuscript.pdf | Lyka Vejano | v1.0 | 🔵 Reserved |
| CI-22 | .gitignore | Dependencies & Env | /.gitignore | Reymark Boado | v1.0 | 🟢 Active |
| CI-23 | requirements.txt | Dependencies & Env | /Dependencies and Environment/requirements.txt | Reymark Boado | v1.0 | 🟢 Active |
| CI-24 | environment.yml | Dependencies & Env | /Dependencies and Environment/environment.yml | Reymark Boado | v1.0 | 🟢 Active |
| CI-25 | python-version.txt | Dependencies & Env | /Dependencies and Environment/python-version.txt | Reymark Boado | v1.0 | 🟢 Active |
| CI-26 | SETUP_GUIDE.md | Dependencies & Env | /Dependencies and Environment/SETUP_GUIDE.md | Reymark Boado | v1.0 | 🟢 Active |
| CI-27 | RUNBOOK.md | Dependencies & Env | /Dependencies and Environment/RUNBOOK.md | Reymark Boado | v1.0 | 🟢 Active |
| CI-28 | training_pipeline.ipynb | Dependencies & Env | /Dependencies and Environment/colab_notebooks/training_pipeline.ipynb | Reymark Boado | v1.0 | 🟡 Under Development |
| CI-29 | colab notebooks README.md | Dependencies & Env | /Dependencies and Environment/colab_notebooks/README.md | Reymark Boado | v1.0 | 🟢 Active |
| CI-30 | DATA_SCHEMA.md | Data & Schema | /Data and Schema/DATA_SCHEMA.md | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-31 | data_manifest.md | Data & Schema | /Data and Schema/data_manifest.md | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-32 | reference_sources.md | Data & Schema | /Data and Schema/reference_sources.md | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-33 | study_area_boundary.geojson | Data & Schema | /Data and Schema/samples/study_area_boundary.geojson | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-34 | sample_labels.geojson | Data & Schema | /Data and Schema/samples/sample_labels.geojson | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-35 | sample_patch_index.csv | Data & Schema | /Data and Schema/samples/sample_patch_index.csv | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-36 | sample_metrics.example.json | Data & Schema | /Data and Schema/samples/sample_metrics.example.json | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-37 | MODEL_CARD.md | Model Artifact | /Model/MODEL_CARD.md | Nash Francis Caluza | v1.0 | 🟡 Under Development |
| CI-38 | metrics.example.json | Model Artifact | /Model/metrics.example.json | Nash Francis Caluza | v1.0 | 🟢 Active |
| CI-39 | metrics.json | Model Artifact | /Model/metrics.json | Nash Francis Caluza | v1.0 | 🔵 Reserved |
| CI-40 | weights/ | Model Artifact | /Model/weights/ | Nash Francis Caluza | v1.0 | 🟡 Under Development |

### Status Legend

- 🟡 **Under Development** — active coding or training in progress; item not yet through a full revision cycle.
- 🟣 **Revised (Post-Proposal)** — item has been updated to incorporate the evaluators' comments from the thesis proposal defense; revision round complete, awaiting re-baselining / adviser re-approval.
- 🟢 **Active** — baseline approved and operational for development/production.
- 📝 **Draft** — initial documentation undergoing review.
- 🔵 **Reserved** — allocated placeholder directory/file for future artifacts.

### Change Control Protocol

- Any modification to a CI increments its version and updates its Lifecycle Status in this register.
- The commit message must reference the CI ID (e.g., `CI-11: revise evaluation split persistence — v1.1`).
- Status transitions:
  - Development path: 🔵 Reserved → 🟡 Under Development → 🟣 Revised (Post-Proposal) → 🟢 Active
  - Documentation path: 🔵 Reserved → 📝 Draft → 🟣 Revised (Post-Proposal) → 🟢 Active
- An item returns to 🟡 Under Development whenever rework opens again.
- Items updated in response to thesis proposal defense panel comments must be marked 🟣 Revised (Post-Proposal) once the revision round for that item is complete, and the revision round must be logged in Version History.
- Large binary artifacts (rasters, patches, weights) are tracked via the Drive locations recorded in `Data and Schema/data_manifest.md`; only their register entries change in Git.

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

## 🧭 How to Use the System

This section explains what actually happens when someone uses the system, from opening the browser to getting a report.

### For a MENRO officer or reviewer (using the finished web prototype)

1. **Open the dashboard** (`/`) — this is the landing page. It shows the study area, the observation period (2019–2024), and a quick summary of whether the underlying model has been trained yet (currently demo data).
2. **Check Annual Maps** (`/maps`) — pick a year, and the system displays that year's mangrove vs. non-mangrove map directly on an interactive Leaflet map, so you can zoom into specific parts of Barangay Dulao.
3. **Check Change Detection** (`/change`) — pick two consecutive years (e.g., 2021 and 2022), and the system overlays where mangrove was gained, lost, or stayed the same, along with the area in hectares for each category.
4. **Review Statistics** (`/statistics`) — see cover trends across all years as charts, plus a full transition table summarizing gain and loss for every year-pair.
5. **Check Model Evaluation** (`/model`) — view the model's actual performance: F1-score, IoU, mAP, and the precision-recall curve, so the numbers behind the maps aren't a black box.
6. **Download a Report** (`/report`) — generates a PDF summary of the above, meant to be handed to MENRO leadership or filed for record-keeping.

### For a developer (running or extending the pipeline)

The pipeline scripts in `SourceCode/preprocessing/` are meant to be run in this order, each one feeding into the next:

1. `gee_export.py` — pulls raw Sentinel-2 imagery for the chosen years.
2. `make_patches.py` — turns that raw imagery into the 256×256, 5-channel patches the model actually trains on.
3. `rasterize_labels.py` — turns MENRO-validated mangrove boundaries into the matching binary label patches.
4. `train.py` — trains U-Net using the patches and labels from steps 2–3.
5. `evaluate.py` — scores the trained model and locks the final classification threshold.
6. `change_detection.py` — once a model is trained and locked, this compares any two years' outputs to produce gain/loss statistics.

Each script currently writes output that the Flask app (`app.py`) will eventually read directly — right now, `app.py` serves demo data instead, with each integration point marked `>>> INTEGRATION` in the code so it's obvious where real pipeline output will plug in later.

> **Note:** the pipeline scripts above are at v1 and under revision — this run order describes the finished workflow they will perform once finalized.

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
