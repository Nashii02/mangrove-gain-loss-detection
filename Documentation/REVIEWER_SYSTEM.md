# Software Engineering Defense & Professor Review Guide: Mangrove Gain & Loss Detection System

**Course:** Software Engineering / Computer Science Undergraduate Capstone & Thesis Defense  
**Target Reviewer:** University-Level Software Engineering Professor / Technical Panelists  
**System:** Deep Learning-Based Detection of Mangrove Gain and Loss in Barangay Dulao, Aringay, La Union  
**Authors:** Caluza, Nash Francis M. · Boado, Reymark O. · Vejano, Lyka B. (BSCS, DMMMSU-SLUC)

---

## Executive Overview for the Presenting Team

A Software Engineering professor does not evaluate your project as a generic municipal user. While MENRO cares about *"Is this easy to understand?"*, an SE professor cares about:
1. **Architectural Rigor & Separation of Concerns (SoC):** Is your system structured logically, or is it a tangled monolithic ball of mud?
2. **Data Integrity & State Invariants:** Can your system produce impossible, contradictory, or mathematically broken states?
3. **API Design & Contract Consistency:** Are your client-server boundaries RESTful, idempotent, and type-safe?
4. **Integration Reality vs. Simulation:** Are you honest about what is executed online versus offline, and what architectural decisions justify that separation?
5. **Geospatial & Computational Soundness:** Do you understand coordinate projections, pixel resolutions, and spatial transformations, or are you just displaying pretty shapes on Leaflet?

This document arms you with the **exact questions your professor will ask**, the **flawless academic answers** you must give, and a **comprehensive technical jargon lexicon** to demonstrate senior-level software engineering fluency.

---

## Table of Contents
1. [Core Defense Questions by Architectural Domain](#1-core-defense-questions-by-architectural-domain)
   - [Domain A: Software Architecture & Design Patterns](#domain-a-software-architecture--design-patterns)
   - [Domain B: Data Invariants & Domain Consistency](#domain-b-data-invariants--domain-consistency)
   - [Domain C: ML Pipeline Integration & Offline vs. Online Inference](#domain-c-ml-pipeline-integration--offline-vs-online-inference)
   - [Domain D: Geospatial Computing & Coordinate Reference Systems](#domain-d-geospatial-computing--coordinate-reference-systems)
   - [Domain E: Asynchronous Frontend-Backend Communication](#domain-e-asynchronous-frontend-backend-communication)
   - [Domain F: Security, Concurrency & Resource Management](#domain-f-security-concurrency--resource-management)
2. [Rapid-Fire Professor Grilling Simulation (20 Tough Questions)](#2-rapid-fire-professor-grilling-simulation)
3. [Master Academic Jargon & Lexicon](#3-master-academic-jargon--lexicon)
4. [Oral Defense Rehearsal Strategy & Tactics](#4-oral-defense-rehearsal-strategy--tactics)

---

# 1. Core Defense Questions by Architectural Domain

---

### Domain A: Software Architecture & Design Patterns

#### Q1.1: "Walk me through the high-level architecture of your system. What architectural pattern does this follow, and why did you choose it?"
- **Professor's Intent:** Testing whether you understand architectural styles (Layered, MVC, Microservices) or simply threw scripts into a folder.
- **Your Answer:**
  > "Our system implements a **Decoupled Multi-Layered Architecture** adhering to the **Model-View-Controller (MVC)** architectural pattern, integrated with a **Service-Oriented Batch Pipeline**:
  > 1. **Presentation Layer (View):** Client-side HTML5/Bootstrap 5 templates rendered via Jinja2, utilizing Leaflet.js for vector geospatial visualization and Chart.js for analytical plotting.
  > 2. **Application & Routing Layer (Controller):** A Python Flask WSGI microframework handling HTTP request dispatching, input validation, context injection, and RESTful routing.
  > 3. **Domain & Business Logic Layer (Model):** Independent modules encapsulating domain rules: the **Spatial Transition Engine** that enforces conservation of mass across a 4-class partition, the **ReportLab Platypus Engine** for dynamic document compilation, and the **Authoritative Geometry Subsystem** in `config.py`.
  > 4. **Offline Deep Learning Subsystem:** An asynchronous, disconnected pipeline (GEE, Rasterio, TensorFlow/Keras) handling satellite image ingestion, patching, and binary segmentation.
  > 
  > We chose this architecture because it achieves **High Cohesion** within the web application and **Loose Coupling** between the interactive presentation tier and the computationally intensive deep-learning pipeline."
- **Key Jargon to Use:**
  - *Separation of Concerns (SoC)*
  - *Model-View-Controller (MVC)*
  - *High Cohesion & Loose Coupling*
  - *Layered Tiered Architecture*
  - *Decoupled Execution Pipeline*

---

#### Q1.2: "Why did you use Flask instead of Django, FastAPI, or a full-stack framework like Next.js?"
- **Professor's Intent:** Testing your technology selection justification.
- **Your Answer:**
  > "We conducted a trade-off analysis based on our functional requirements:
  > - **Against Django:** Django provides an Object-Relational Mapping (ORM) and administrative engine designed for transactional relational databases. Our domain model does not require complex relational schemas or user authentication tables; it processes geospatial GeoJSON features, numerical raster arrays, and in-memory document streams. Django’s overhead would introduce unnecessary bloat.
  > - **Against FastAPI:** While FastAPI provides high-throughput asynchronous request handling via ASGI, our web tier is an environmental decision-support system for a small municipal department (MENRO), not a high-concurrency microservice handling thousands of requests per second. Flask 3.0 provides synchronous simplicity, mature Jinja2 template integration, and seamless interoperability with scientific libraries (NumPy, Rasterio, ReportLab).
  > - **Against Next.js:** Keeping the backend in Python allows direct execution of Python-native geospatial libraries (GeoPandas, Shapely, ReportLab) without requiring a multi-language polyglot microservice bridge."
- **Key Jargon to Use:**
  - *Architectural Trade-Off Analysis*
  - *Over-Engineering vs. Fit-for-Purpose*
  - *Object-Relational Mapping (ORM) Overhead*
  - *WSGI vs. ASGI Runtime Semantics*
  - *Polyglot Architecture Complexity*

---

### Domain B: Data Invariants & Domain Consistency

#### Q1.3: "In change detection, how do you prevent mathematical inconsistencies where gain and loss don't match the annual totals?"
- **Professor's Intent:** Pouncing on the common student flaw of computing $\text{Gain} = \max(0, A_2 - A_1)$ and $\text{Loss} = \max(0, A_1 - A_2)$, which ignores spatial gross changes.
- **Your Answer:**
  > "We established a strict **State Invariant** rooted in the **Conservation of Spatial Extent**. In remote sensing change detection over a fixed study boundary, the spatial extent partitions into four mutually exclusive categories:
  > $$\text{Total Area} = \text{Stable Mangrove} + \text{Mapped Gain} + \text{Mapped Loss} + \text{Stable Non-Mangrove}$$
  > 
  > In `Source_Code/app.py`, we enforce three fundamental domain conservation laws:
  > 1. $\text{Area}(Y_1) = \text{Stable Mangrove} + \text{Mapped Loss}$
  > 2. $\text{Area}(Y_2) = \text{Stable Mangrove} + \text{Mapped Gain}$
  > 3. $\text{Net Change} = \text{Mapped Gain} - \text{Mapped Loss} = \text{Area}(Y_2) - \text{Area}(Y_1)$
  > 
  > To ensure complete integrity across all 15 valid comparison pairs, `get_demo_change()` executes automated runtime assertions checking that:
  > $$\text{abs}((\text{Stable} + \text{Gain} + \text{Loss} + \text{Stable Non-Mangrove}) - 316.74) < 0.01$$
  > If any transition calculation violates this invariant by even $0.01\text{ ha}$, the backend triggers an assertion error and refuses to serve corrupted data."
- **Key Jargon to Use:**
  - *Domain Invariants & State Consistency*
  - *Conservation of Spatial Extent*
  - *Mutually Exclusive and Collectively Exhaustive (MECE) Partition*
  - *Gross vs. Net Flux Dynamics*
  - *Runtime Assertion & Defensive Programming*

---

#### Q1.4: "How do you handle floating-point arithmetic errors in your area computations?"
- **Professor's Intent:** Checking if you know about IEEE 754 floating-point inaccuracies (`0.1 + 0.2 = 0.30000000000000004`).
- **Your Answer:**
  > "Because Python floats and JavaScript numbers use IEEE 754 double-precision representation, raw accumulations can accumulate infinitesimal rounding drift. We address this at three architectural points:
  > 1. **At the calculation layer:** We enforce explicit rounding to two decimal places (`round(value, 2)`) at each transition step, matching our sensor precision ($10\text{ m} \times 10\text{ m} = 0.01\text{ ha}$).
  > 2. **At assertion checkpoints:** We avoid direct equality checks (`==`) and instead use delta comparisons with an epsilon tolerance: `abs(actual - expected) < 0.01`.
  > 3. **At the presentation layer:** In JavaScript, the `fmt()` utility normalizes numbers using `Number.toLocaleString(undefined, { maximumFractionDigits: 2 })`, ensuring localized formatting without floating-point artifacts."
- **Key Jargon to Use:**
  - *IEEE 754 Double-Precision Floating-Point Standard*
  - *Accumulator Precision Drift*
  - *Epsilon Tolerance Comparison*
  - *Canonical Numerical Normalization*

---

### Domain C: ML Pipeline Integration & Offline vs. Online Inference

#### Q1.5: "Why is your U-Net model not doing live inference inside the Flask web app when a user selects a year?"
- **Professor's Intent:** Trying to trap you into pretending the model runs live, or criticizing your architecture for being disconnected.
- **Your Answer:**
  > "That is a deliberate and principled software engineering decision: **Offline Batch Pre-computation versus Online Request-Driven Inference**:
  > 1. **Resource Constraints & Latency:** Ingesting a 5-band Sentinel-2 multispectral scene across the Dulao boundary requires cloud masking, SWIR bilinear resampling, NDVI calculation, tiling into $256 \times 256$ patches, and executing deep convolutional neural network forward passes. Executing this synchronously inside a web request worker would take 30 to 90 seconds, causing browser HTTP socket timeouts and thread starvation in the Flask WSGI server.
  > 2. **Memory Footprint:** Loading TensorFlow/Keras and model weights into a web server process inflates the resident memory footprint to over 1.5 GB per worker thread.
  > 3. **Domain Realities:** Satellite observations for environmental monitoring are **temporal baselines**, not real-time streaming data. Sentinel-2 scenes are captured on a 5-day revisit cycle, and our methodology selects one cloud-free composite per annual dry season. Therefore, computing annual classification masks is inherently an **offline batch job**.
  > 4. **Architecture:** The model pipeline runs offline in a GPU-accelerated cloud environment (Google Colab), outputs binary GeoTIFF classification masks (`MASK_{year}.tif`), and the web application serves these pre-computed, verified analytical outputs with sub-second response times."
- **Key Jargon to Use:**
  - *Batch Pre-computation vs. Real-Time Online Inference*
  - *Thread Starvation & WSGI Worker Blocking*
  - *Resident Set Size (RSS) Memory Overhead*
  - *Temporal Baseline vs. Streaming Telemetry*
  - *Sub-second Latency SLA (Service Level Agreement)*

---

#### Q1.6: "What is your U-Net architecture, and why did you use 5 channels instead of standard RGB?"
- **Professor's Intent:** Testing your domain machine learning understanding.
- **Your Answer:**
  > "Our architecture is an encoder-decoder Fully Convolutional Network (FCN) with symmetric skip connections, following Ronneberger et al. (2015):
  > - **Input Tensor:** $256 \times 256 \times 5$ pixels.
  > - **Channels:** Band 3 (Green, 560 nm), Band 4 (Red, 665 nm), Band 8 (Near-Infrared, 842 nm), Band 11 (Short-Wave Infrared, 1610 nm), and the derived Normalized Difference Vegetation Index (NDVI).
  > - **Channel Justification:** Standard 3-channel RGB is completely insufficient for coastal wetland classification. Mangroves exhibit a severe spectral reflectance spike in NIR (Band 8) due to spongy mesophyll leaf structure, while open water absorbs NIR completely. Band 11 (SWIR) is critical because it responds to moisture and tidal inundation, separating mangroves from terrestrial vegetation. NDVI isolates chlorophyll density.
  > - **Network Layers:** 4 encoder blocks (64 to 512 filters, ReLU, $2 \times 2$ Max Pooling), a 1024-filter bottleneck, and 4 decoder blocks with $2 \times 2$ transposed convolutions concatenated with encoder feature maps via skip connections to preserve high-resolution spatial boundary delineations.
  > - **Output:** A $256 \times 256 \times 1$ tensor activated by Sigmoid, yielding pixel-wise mangrove probabilities $P \in [0, 1]$."
- **Key Jargon to Use:**
  - *Fully Convolutional Network (FCN)*
  - *Spectral Signature & Spectral Reflectance Characteristics*
  - *Near-Infrared (NIR) & Short-Wave Infrared (SWIR) Absorption Bands*
  - *Skip Connections & Spatial Feature Preservation*
  - *Continuous Probability Topology (Sigmoid Activation)*

---

### Domain D: Geospatial Computing & Coordinate Reference Systems

#### Q1.7: "Why can't you calculate mangrove area directly in EPSG:4326 (Latitude/Longitude degrees)?"
- **Professor's Intent:** Catching students who don't understand map projections and compute planar geometry using spherical angular coordinates.
- **Your Answer:**
  > "Because **EPSG:4326 (WGS 84)** is a **Geodetic Coordinate Reference System** expressed in angular units (degrees of latitude and longitude), not planar linear units (meters). 
  > 
  > At the equator, 1 degree of longitude is roughly 111.32 km, but as latitude increases, meridians converge:
  > $$\Delta x = 111.32 \times \cos(\text{latitude}) \text{ km}$$
  > At Barangay Dulao ($16.37^\circ\text{N}$), 1 degree of longitude is only approximately $106.8\text{ km}$, while 1 degree of latitude is $110.6\text{ km}$. Calculating polygon areas directly in degrees produces mathematically distorted, non-uniform trapezoidal planar errors.
  > 
  > Therefore:
  > 1. All raw satellite scenes and area calculations are projected into **UTM Zone 51N (EPSG:32651)**, a **Conformal Transverse Mercator Projection** using Cartesian meters.
  > 2. On this metric grid, our Sentinel-2 pixel size is exactly $10\text{ m} \times 10\text{ m} = 100\text{ m}^2 = 0.01\text{ hectares}$.
  > 3. We only project into EPSG:4326 when generating GeoJSON for Leaflet.js, because web mapping tile layers (Leaflet/OpenStreetMap) render in WGS 84 / Web Mercator (EPSG:3857)."
- **Key Jargon to Use:**
  - *Geodetic vs. Projected Coordinate Reference System (CRS)*
  - *Meridian Convergence & Latitudinal Distortion*
  - *Universal Transverse Mercator (UTM Zone 51N / EPSG:32651)*
  - *Conformal Cartesian Metric Projection*
  - *Raster Affine Transformation Matrix*

---

### Domain E: Asynchronous Frontend-Backend Communication

#### Q1.8: "How does your client handle asynchronous race conditions if a user clicks 'Detect Changes' multiple times rapidly?"
- **Professor's Intent:** Testing frontend engineering, UI state management, and event handling.
- **Your Answer:**
  > "We implement a **Defensive UI State Transition Pattern** in `Source_Code/static/js/map_change.js`:
  > 1. **Immediate Mutex Locking:** The moment `loadChange()` is invoked, the button triggers `btnLoad.disabled = true;` and replaces the icon with an animated Bootstrap spinner. This physically prevents subsequent click events from queueing overlapping HTTP requests.
  > 2. **DOM Reset & Skeleton State:** Metric cards are immediately reset to placeholder ellipses (`'…'`) to prevent stale data from lingering if a network interruption occurs.
  > 3. **Layer Cleanup:** Previous Leaflet GeoJSON layer references are cleaned up via `if (changeLayer) mapChange.removeLayer(changeLayer);` prior to adding newly fetched vector layers.
  > 4. **Deterministic Completion:** In a `finally` block, `btnLoad.disabled = false;` restores interactivity only after the response has been completely processed or trapped by the error handler."
- **Key Jargon to Use:**
  - *Asynchronous Race Condition*
  - *Defensive UI State Transition*
  - *Mutex Locking & Button Throttling*
  - *Deterministic Teardown (`finally` block)*
  - *Stale Data Masking*

---

#### Q1.9: "Are your REST APIs idempotent? What HTTP status codes do you return?"
- **Professor's Intent:** Testing your API design against HTTP/1.1 specifications.
- **Your Answer:**
  > "Yes, our API strictly follows RESTful idempotency principles:
  > - **`GET /api/annual/<year>` and `GET /api/change/<y1>/<y2>`:** These are strictly read-only safe and idempotent methods. Executing them 1 time or 1,000 times produces identical server state and identical JSON responses.
  > - **`POST /api/report`:** We use `POST` because the client triggers document compilation. While it is functionally idempotent (generating a PDF based on the static baseline), `POST` is semantically appropriate for document creation workflows according to RFC 9110.
  > 
  > **HTTP Status Codes:**
  > - `200 OK`: Request succeeded, returns JSON or PDF binary stream.
  > - `400 Bad Request`: Client parameter violation (e.g., requesting identical years $y_1 == y_2$, or non-chronological pairs $y_1 > y_2$). Returns a descriptive JSON error payload.
  > - `404 Not Found`: Temporal parameter out of scope (e.g., year outside 2019–2024).
  > - `500 Internal Server Error`: Unhandled server-side exception, trapped and logged."
- **Key Jargon to Use:**
  - *RESTful Idempotency & Safety Semantics (RFC 9110)*
  - *HTTP Status Code Conformance*
  - *Payload Validation & Semantic Routing*
  - *Richardson Maturity Model Level 2*

---

### Domain F: Security, Concurrency & Resource Management

#### Q1.10: "If 100 users hit 'Download PDF' simultaneously, what happens to your server?"
- **Professor's Intent:** Stress-testing your resource management awareness.
- **Your Answer:**
  > "Under our current development WSGI server (Flask development server), requests are handled synchronously or across a limited thread pool, meaning 100 concurrent requests would experience serialization and queuing latency.
  > 
  > Furthermore, `report_generator.py` compiles multi-page PDFs using ReportLab Platypus flowables entirely in an in-memory `io.BytesIO` buffer. While this avoids disk I/O bottlenecks and temporary file race conditions, allocating 100 simultaneous ReportLab document instances (each holding ~5–10 MB of layout trees, graphics drawings, and fonts in heap memory) could consume up to 1 GB of RAM, risking Out-Of-Memory (OOM) worker termination.
  > 
  > **Production Remediation Architecture:**
  > In a production deployment, we would:
  > 1. Run Flask behind a production WSGI container like **Gunicorn** with 4 worker processes and gevent worker classes.
  > 2. Implement **Rate Limiting** via `Flask-Limiter` (e.g., max 5 PDF generations per minute per client IP).
  > 3. Offload PDF compilation to an asynchronous task queue (e.g., **Celery** backed by **Redis**), returning a task ID and polling status, rather than compiling on the main web request thread."
- **Key Jargon to Use:**
  - *Thread Starvation & Concurrency Bottlenecks*
  - *Heap Memory Allocation & OOM (Out Of Memory) Risk*
  - *WSGI Containerization (Gunicorn / uWSGI)*
  - *Rate Limiting & Token Bucket Algorithms*
  - *Asynchronous Message Queue Task Offloading (Celery/Redis)*

---

# 2. Rapid-Fire Professor Grilling Simulation

Here are 20 aggressive, direct questions your professor might throw at your team during defense, with exact tactical answers:

| # | Professor's Attack Question | Quick Tactical Academic Answer |
|---|---|---|
| **1** | *"Where are your trained U-Net `.keras` weights right now?"* | *"They are not in the repository yet. Model training is an offline batch pipeline requiring GPU compute; the repository currently holds the validated model architecture and training scripts (`unet_model.py`, `train.py`). Weights will be placed in `Model/weights/` once reference mask validation with MENRO is finalized."* |
| **2** | *"If the model isn't trained yet, how are you displaying gain and loss maps?"* | *"The web application is operating in an explicit, isolated **Demo Mode** (`DEMO_MODE=True`). It uses an approved baseline scenario with synthetic scalable polygon vectors to validate user interaction, UI contracts, and report generation."* |
| **3** | *"Aren't these gain and loss numbers just made up then?"* | *"No. They are synthetic demonstration values, but they are governed by strict mathematical conservation rules where $\text{Stable} + \text{Gain} + \text{Loss} + \text{Stable Non-Mangrove} == 316.74\text{ ha}$ with $0.00$ discrepancy across all 15 comparison intervals."* |
| **4** | *"Why did you make a 25-point polygon instead of a simple bounding box?"* | *"A rectangular bounding box includes inland residential zones and extensive deep-sea areas, skewing spatial statistics. The authoritative 25-point polygon strictly isolates Barangay Dulao's estuarine and intertidal coastal boundary."* |
| **5** | *"Why is the area of Dulao exactly 316.74 hectares?"* | *"When the 25 geographic coordinates are projected from WGS 84 into the regional metric projection UTM Zone 51N (EPSG:32651), the planar polygon calculates to $3,167,439.71\text{ m}^2$, which divides by 10,000 to yield exactly $316.74\text{ ha}$."* |
| **6** | *"What is the spatial resolution of your satellite data?"* | *"10 meters per pixel for bands B3, B4, and B8. Band 11 is natively 20 meters, which we bilinearly resample to 10 meters. Thus, 1 pixel equals $100\text{ m}^2$ or $0.01\text{ hectares}$."* |
| **7** | *"What happens if a user compares 2024 to 2019 (backwards)?"* | *"The client dropdown prevents inverted selections automatically. If an external client sends a manual HTTP request to `/api/change/2024/2019`, the backend rejects it with an HTTP 400 Bad Request error."* |
| **8** | *"Why is `/model` not in your navigation bar?"* | *"In our stakeholder design for Aringay MENRO, non-technical officers are sheltered from internal neural network metrics to prevent cognitive overload. The `/model` route is preserved as an administrative diagnostic view for technical reviewers and academic defense."* |
| **9** | *"What loss function does your U-Net use?"* | *"Binary Cross-Entropy (`binary_crossentropy`), optimized with Adam at a learning rate of $0.001$, as specified in thesis methodology."* |
| **10** | *"How do you evaluate model performance?"* | *"Using a validation split (20%), sweeping classification thresholds from $0.05$ to $0.95$ in steps of $0.05$. We identify the threshold maximizing validation Intersection over Union (IoU) and compute Mean Average Precision (mAP) and F1-score."* |
| **11** | *"What is IoU in plain terms?"* | *"Intersection over Union, or the Jaccard Index: the area of overlap between model prediction and ground truth divided by the area of union. It penalizes both false positives and false negatives."* |
| **12** | *"Why did you create a standalone PDF generator instead of using browser `window.print()`?"* | *"`window.print()` is non-deterministic; it depends on local browser margins, zoom levels, CSS print-media queries, and cannot generate official multi-page municipal certificates with standardized signature lines and page counters."* |
| **13** | *"How does the system ensure non-technical MENRO users understand the data?"* | *"By eliminating all technical acronyms (`ha`, `ROI`, `IoU`, `F1`) and introducing everyday scale equivalents ($\text{hectares} \times 1.4 \approx \text{football fields}$) alongside a 3-step comparison wizard."* |
| **14** | *"Why does your `config.py` contain `/content/` paths?"* | *"Those reflect the execution environment on Google Colab GPU runtimes for offline training. For local execution, paths are resolved relative to `Path(__file__)`."* |
| **15** | *"What is your Git branching and versioning strategy?"* | *"Semantic Versioning (v1.0.0 prototype), separating presentation web code from offline deep learning preprocessing under our Configuration Management Plan."* |
| **16** | *"What database are you using?"* | *"The prototype currently uses structured, schema-validated flat files (`outputs/history.json` and static lookup tables) for zero-dependency portability during municipal evaluations. Production will migrate to PostgreSQL/PostGIS."* |
| **17** | *"How do you test your software?"* | *"Verification and validation: runtime assertion tests checking the 316.74 ha spatial conservation invariant across all 15 pairs, automated HTTP status code validation, and client-side error trap testing."* |
| **18** | *"What is the significance of the dry season window (Feb 1 - Apr 30)?"* | *"Tropical coastal satellite imagery suffers from heavy monsoon cloud occlusion. Dry-season scenes offer sub-20% cloud cover and optimal solar elevation angles, minimizing tidal and atmospheric variance."* |
| **19** | *"Can a user upload a drone image to your web app right now?"* | *"No. The system is designed as an environmental reporting dashboard for calibrated Sentinel-2 satellite baselines, not an arbitrary uncalibrated RGB image segmentation tool."* |
| **20** | *"What is your single most important contribution in this prototype?"* | *"Translating complex, multi-temporal satellite deep-learning observations into a mathematically consistent, accessible decision-support system that empowers local municipal officers to protect coastal ecosystems."* |

---

# 3. Master Academic Jargon & Lexicon

Use these terms naturally in your presentation to demonstrate high-level technical mastery:

| Technical Jargon Term | Precise Definition | How to Use It in Your Oral Defense |
|---|---|---|
| **Separation of Concerns (SoC)** | An architectural design principle for separating a computer program into distinct sections, such that each section addresses a separate concern. | *"We enforced strict Separation of Concerns between our offline ML ingestion pipeline and our Flask web presentation tier."* |
| **State Invariant** | A condition that must always be true during the execution of a program or within a domain model. | *"The 316.74-hectare total area is an architectural state invariant that is verified at runtime before data reaches the client."* |
| **Idempotence** | An operation that can be applied multiple times without changing the result beyond the initial application. | *"Our `/api/change/<y1>/<y2>` endpoints are strictly idempotent and read-only, conforming to RFC 9110."* |
| **Coordinate Reference System (CRS)** | A coordinate-based local, regional or global system used to locate geographical entities. | *"We transformed our vectors from geodetic EPSG:4326 to projected Cartesian UTM Zone 51N (EPSG:32651) to eliminate latitudinal area distortion."* |
| **Fully Convolutional Network (FCN)** | A neural network architecture composed exclusively of convolutional layers, enabling pixel-wise dense predictions. | *"Our U-Net is a 5-channel Fully Convolutional Network that maps spatial input tensors directly to probability density rasters."* |
| **Intersection over Union (IoU)** | A metric evaluating semantic segmentation accuracy (also known as the Jaccard Index) measuring overlap between target and prediction. | *"We locked our operating classification threshold at the specific probability that maximizes validation Intersection over Union."* |
| **Affine Transformation** | A geometric transformation in spatial rasters mapping pixel row/column coordinates to projected spatial coordinates. | *"Rasterio uses the GeoTIFF's affine transformation matrix to align image patches with ground truth masks."* |
| **Bilinear Resampling** | A spatial resampling algorithm that uses distance-weighted averages of four nearest pixels to interpolate resolution. | *"We applied bilinear resampling to upsample Sentinel-2 Band 11 from its native 20 m grid to the target 10 m baseline."* |
| **Platypus Flowables** | The Page Layout and Typography Using Scripts engine inside ReportLab that models documents as dynamic printable flow objects. | *"Our PDF reports are programmatically generated via Platypus flowable hierarchies within an in-memory byte buffer."* |
| **WSGI Worker Starvation** | A condition where web server worker threads become exhausted waiting for long-running blocking synchronous jobs. | *"Offline batching avoids WSGI worker thread starvation that would otherwise occur if deep learning inference ran inside HTTP requests."* |
| **Defensive Programming** | A design approach ensuring the continuing function of a piece of software under unforeseen circumstances. | *"We practiced defensive programming by implementing mutex locks on client submission triggers and assert validation on the backend."* |
| **Mutually Exclusive & Collectively Exhaustive (MECE)** | A principle stating that a set of events or categories must partition a space completely with zero overlaps and zero gaps. | *"Our 4-class change detection categories are mathematically MECE, partitioning the 316.74-hectare territory completely."* |
| **Graceful Degradation** | The ability of a computer system to maintain limited functionality even when a large portion of it has been destroyed or is inoperative. | *"If historical logs fail to read from disk, `api_history()` gracefully degrades by generating fallback audit intervals dynamically."* |
| **Z-Ordering** | The ordering of overlapping two-dimensional visual objects along the z-axis (depth). | *"In `_demo_change_geojson()`, we enforce strict Z-ordering so that background non-mangrove vectors do not occlude clickable vegetation patches."* |

---

# 4. Oral Defense Rehearsal Strategy & Tactics

### 1. The "Transparency" Rule
- **Never pretend a mock feature is real.** If the professor asks, *"Are you running U-Net right now on my click?"*, answer immediately: *"No sir/ma'am, the web app is running in Demo Mode using an approved baseline dataset, while model training is an offline batch pipeline."* Professors respect engineering honesty; they destroy students who try to bluff.

### 2. The "Architecture-First" Framing
- When explaining the project, start with the **System Architecture Diagram** (Part 2 of this document). Show that you conceived the system as a whole engineering lifecycle, not just a weekend script.

### 3. Emphasize Domain Invariants
- Spend 60 seconds explaining why $\text{Stable} + \text{Gain} + \text{Loss} + \text{Stable Non-Mangrove} = 316.74\text{ ha}$. Professors love mathematical proofs and invariant preservation because it proves your software isn't just generating arbitrary numbers.

### 4. Divide and Conquer Among Team Members
- **Member 1 (Caluza, Nash Francis M.):** Lead architecture, Flask API routes, invariant math, and system design.
- **Member 2 (Boado, Reymark O.):** Machine learning pipeline, U-Net architecture, spectral bands (B3, B4, B8, B11, NDVI), and evaluation metrics.
- **Member 3 (Vejano, Lyka B.):** Frontend UX, Leaflet mapping, ReportLab PDF compilation, and municipal MENRO operational usability.

---

*End of Reviewer Guide. Refer to [`Documentation/SYSTEM_ARCHITECTURE_AND_OPERATION.md`](file:///c:/Users/Nash%20Francis/caluzanash/Thesis/PROTOTYPE/mangrove-gain-loss-detection/Documentation/SYSTEM_ARCHITECTURE_AND_OPERATION.md) for the complete 31-section technical implementation manual.*
