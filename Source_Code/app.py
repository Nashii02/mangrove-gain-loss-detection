"""
Mangrove Monitoring System — Prototype
Deep Learning-Based Detection of Mangrove Gain and Loss
Brgy. Dulao, Aringay, La Union (Sentinel-2, 2019–2024)

Frontend-serving Flask app. All /api/* endpoints currently return DEMO data.
Search for ">>> INTEGRATION" comments — replace those blocks with the real
ML pipeline outputs (rasterio masks, U-Net predictions, metrics JSON).
"""
import io, json, os
from flask import Flask, render_template, jsonify, request, send_file

import numpy as np

app = Flask(__name__)

YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
STUDY_AREA = {"name": "Barangay Dulao, Aringay, La Union",
              "bbox": [120.355, 16.305, 120.375, 16.325]}   # [W, S, E, N]

MASK_DIR = "data/masks"        # MASK_{year}.tif  (your Part 2b outputs)
MODEL_PATH = "models/final_model.keras"
METRICS_PATH = "data/evaluation/metrics.json"   # saved by your evaluation script

# ───────────────────────── helpers ─────────────────────────

def _demo_blob(year, dx=0.0, dy=0.0, ring=True):
    """Demo mangrove polygon near Dulao. DELETED once real masks are wired in."""
    base = [[120.360, 16.312], [120.365, 16.310], [120.370, 16.313],
            [120.369, 16.318], [120.363, 16.320], [120.359, 16.317]]
    coords = [[round(x + dx * i * 0.0004, 6), round(y + dy * i * 0.0003, 6)]
              for i, (x, y) in enumerate(base)]
    ring = coords + [coords[0]]
    return {"type": "Polygon", "coordinates": [ring]}

# >>> INTEGRATION 1 — real mask → GeoJSON ---------------------------------
# from rasterio.features import shapes
# from rasterio.warp import transform_geom
# import rasterio
# def mask_to_geojson(year):
#     with rasterio.open(f"{MASK_DIR}/MASK_{year}.tif") as src:
#         mask = src.read(1)
#         geoms = [g for g, v in shapes(mask, mask=(mask == 1),
#                    transform=src.transform) if v == 1]
#     feats = [{"type": "Feature", "properties": {"class": "mangrove"},
#               "geometry": transform_geom(src.crs, "EPSG:4326", g)}
#              for g in geoms]
#     return {"type": "FeatureCollection", "features": feats}
# --------------------------------------------------------------------------

# >>> INTEGRATION 2 — area stats from real pixel counts -------------------
# area_ha = int(mask.sum()) / 100          # thesis: Area(ha) = N / 100
# --------------------------------------------------------------------------

DEMO_AREA_HA = {2019: 14.82, 2020: 14.51, 2021: 14.33,
                2022: 13.97, 2023: 14.28, 2024: 14.61}

# ───────────────────────── pages ─────────────────────────

@app.route("/")
def index():
    return render_template("index.html", years=YEARS, study=STUDY_AREA)

@app.route("/maps")
def annual_maps():
    return render_template("annual_maps.html", years=YEARS, study=STUDY_AREA)

@app.route("/change")
def change_detection():
    return render_template("change_detection.html", years=YEARS, study=STUDY_AREA)

@app.route("/statistics")
def statistics():
    return render_template("statistics.html", years=YEARS)

@app.route("/model")
def model_evaluation():
    return render_template("model_evaluation.html")

@app.route("/report")
def report():
    return render_template("report.html", years=YEARS)

# ───────────────────────── API ─────────────────────────

@app.route("/api/meta")
def api_meta():
    return jsonify({"years": YEARS, "study_area": STUDY_AREA,
                    "pixel_m2": 100, "model": "U-Net (5-band input)",
                    "status": "prototype"})

@app.route("/api/annual/<int:year>")
def api_annual(year):
    if year not in YEARS:
        return jsonify({"error": "year out of range"}), 404
    # DEMO — replace with mask_to_geojson(year) + real pixel count
    idx = YEARS.index(year)
    gj = {"type": "FeatureCollection",
          "features": [{"type": "Feature", "properties": {"class": "mangrove"},
                        "geometry": _demo_blob(year, dx=idx * 0.05, dy=idx * -0.03)}]}
    return jsonify({"year": year, "geojson": gj,
                    "area_ha": DEMO_AREA_HA[year],
                    "pixels": int(DEMO_AREA_HA[year] * 100)})

@app.route("/api/change/<int:y1>/<int:y2>")
def api_change(y1, y2):
    if (y1, y2) not in list(zip(YEARS, YEARS[1:])):
        return jsonify({"error": "only consecutive years are comparable"}), 400
    # DEMO — real version: pixel-wise transition per thesis Table 1
    # gain = (earlier==0) & (later==1); loss = (earlier==1) & (later==0)
    loss_ha = round(max(0.0, DEMO_AREA_HA[y1] - DEMO_AREA_HA[y2]), 2)
    gain_ha = round(max(0.0, DEMO_AREA_HA[y2] - DEMO_AREA_HA[y1]), 2)
    gj = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"class": "gain"},
         "geometry": _demo_blob(y2, dx=0.02)},
        {"type": "Feature", "properties": {"class": "loss"},
         "geometry": _demo_blob(y1, dx=-0.02)}]}
    return jsonify({"y1": y1, "y2": y2, "geojson": gj,
                    "gain_ha": gain_ha, "loss_ha": loss_ha,
                    "stable_mangrove_ha": min(DEMO_AREA_HA[y1], DEMO_AREA_HA[y2]),
                    "stable_non_mangrove_ha": None})   # fill from real counts

@app.route("/api/stats")
def api_stats():
    intervals = [{"interval": f"{a}–{b}",
                  "gain_ha": max(0, DEMO_AREA_HA[b] - DEMO_AREA_HA[a]),
                  "loss_ha": max(0, DEMO_AREA_HA[a] - DEMO_AREA_HA[b])}
                 for a, b in zip(YEARS, YEARS[1:])]
    return jsonify({"per_year": [{"year": y, "area_ha": DEMO_AREA_HA[y]}
                                 for y in YEARS],
                    "per_interval": intervals})

@app.route("/api/metrics")
def api_metrics():
    if os.path.exists(METRICS_PATH):
        return jsonify(json.load(open(METRICS_PATH)))
    # DEMO — replace with metrics.json produced by your evaluation script
    return jsonify({
        "f1": 0.874, "iou": 0.776, "mAP": 0.921,
        "threshold": 0.55, "split": "80/20",
        "config": {"optimizer": "Adam (lr=0.001)",
                   "loss": "binary cross-entropy",
                   "input": "256×256×5 (B3, B4, B8, B11, NDVI)",
                   "output": "sigmoid probability map"},
        "pr_curve": {"recall": [0.0, .32, .58, .74, .85, .92, .96, .98, 1.0],
                     "precision": [1.0, .98, .96, .93, .90, .86, .80, .71, .55]},
        "confusion": {"TP": 41820, "FP": 6024, "FN": 6036,
                      "TN": 110120}})

# >>> INTEGRATION 3 — PDF report (ReportLab) -------------------------------
@app.route("/api/report", methods=["POST"])
def api_report():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, h - 60, "Mangrove Gain and Loss Report — Brgy. Dulao, Aringay, La Union")
    c.setFont("Helvetica", 10)
    c.drawString(50, h - 80, "Sentinel-2 · U-Net segmentation · 2019–2024")
    y = h - 120
    for yr in YEARS:
        c.drawString(60, y, f"{yr}: mapped mangrove cover ≈ {DEMO_AREA_HA[yr]:.2f} ha")
        y -= 16
    c.drawString(50, y - 10, "NOTE: prototype output — figures from demo data.")
    c.showPage(); c.save()
    buf.seek(0)
    return send_file(buf, as_attachment=True,
                     download_name="mangrove_report.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
