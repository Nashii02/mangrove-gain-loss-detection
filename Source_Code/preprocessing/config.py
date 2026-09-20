"""
Central configuration — SINGLE SOURCE OF TRUTH for the entire pipeline.
Values match the unrevised Colab notebook (v1). All other modules import
from here; nothing may redefine ROI / YEARS / prep() locally.

Status: v1 — under revision (see Documentation/03_Data_Acquisition_Protocol.md)
"""
from pathlib import Path

# ── Earth Engine ──────────────────────────────────────────────────────
PROJECT_ID   = "magrove-detection"     # team GEE Cloud Project ID (as created)
COLLECTION   = "COPERNICUS/S2_SR_HARMONIZED"   # 2022+ DN offset pre-harmonized
MAX_CLOUD    = 20                       # scene-level cloud filter (%)
BAND_SCALE   = 10000.0                  # DN → reflectance 0–1

# ── Study area: Brgy. Dulao, Aringay, La Union ────────────────────────
# Un-closed lon/lat ring (EPSG:4326). Mirrors Data and Schema/samples/
# study_area_boundary.geojson — the authoritative copy lives there.
ROI_LONLAT = [
    [120.33213318747562, 16.368938079569283],
    [120.33393563193363, 16.36683809979862],
    [120.33487976950687, 16.367291038523962],
    [120.33629597586673, 16.366426336408516],
    [120.33629597586673, 16.36601457214936],
    [120.3402871028809,  16.363873383993326],
    [120.3429907695679,  16.364820450883474],
    [120.34286202353519, 16.367826328389004],
    [120.34221829337162, 16.36992629752131],
    [120.34191788596195, 16.373220321200336],
    [120.34080208701175, 16.376431940716547],
    [120.34093083304447, 16.377502468799737],
    [120.34037293356937, 16.378325947940613],
    [120.33801258963626, 16.37882003375547],
    [120.33676804465335, 16.380796364491815],
    [120.33384980124515, 16.383266749732627],
    [120.33307732504886, 16.384584275723817],
    [120.33063115042728, 16.384666620802506],
    [120.32977284354251, 16.387136956981955],
    [120.32735516984349, 16.387870006116763],
    [120.32031705338841, 16.386058436129765],
    [120.32246282060032, 16.382311726583545],
    [120.32576730210667, 16.377082681868],
    [120.32722642381077, 16.374323995463598],
    [120.33001592118626, 16.370330007188112],
]

def get_roi(ee):
    """Build the study-area geometry. `ee` is passed in so importing this
    module never triggers an Earth Engine initialization."""
    ring = ROI_LONLAT + [ROI_LONLAT[0]]          # GeoJSON/EE require a closed ring
    return ee.Geometry.Polygon([ring])

# ── Temporal window (fixed dry season, identical every year) ─────────
YEARS      = [2019, 2020, 2021, 2022, 2023, 2024]
START, END = "-02-01", "-04-30"

# ── Patching ─────────────────────────────────────────────────────────
PATCH         = 256     # thesis spec: 256 × 256 patches
MAX_CLOUD_FRAC = 0.10   # thesis: patches with >10% cloud/missing → excluded

# ── Paths (Colab layout; adjust for local runs) ──────────────────────
DRIVE_DIR = Path("/content/drive/MyDrive/GEE_Exports")        # DULAO_{year}.tif
OUT_DIR   = Path("/content/mangrove_project/data")            # working folder
IMAGES_DIR = OUT_DIR / "images"
MASKS_DIR  = OUT_DIR / "masks"
LABELS_DIR = OUT_DIR / "labels"
MODELS_DIR = Path("/content/mangrove_project/models")
METRICS_OUT = Path(__file__).resolve().parents[2] / "Model" / "metrics.json"

for _d in (IMAGES_DIR, MASKS_DIR, LABELS_DIR, MODELS_DIR):
    _d.mkdir(parents=True, exist_ok=True)
