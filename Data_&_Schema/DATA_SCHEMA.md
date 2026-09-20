
Data & Schema Reference
Status: schemas below describe the formats the pipeline will produce.Actual files will be generated after dataset acquisition and preprocessing.

1. Rasters (Google Drive — not in Git)
File	Format	Contents
DULAO_{year}.tif	GeoTIFF, float32, 5 bands, 10 m, EPSG:32xxx (scene CRS)	B3, B4, B8, B11, NDVI (reflectance 0–1); NaN = cloud-masked pixels
MASK_{year}.tif	GeoTIFF, uint8, 1 band	1 = mangrove, 0 = non-mangrove (MENRO-validated reference)
2. Patches (256×256)
File	Shape / dtype	Contents
images/{year}_{row}_{col}.npy	(256, 256, 5) float32	5-channel input; channel order B3, B4, B8, B11, NDVI; values 0–1
masks/{year}_{row}_{col}.npy	(256, 256) float32	1 = mangrove, 0 = non-mangrove; same grid alignment as the image patch
Padding note: rasters smaller than a patch multiple are zero-padded to the nextmultiple of 256; patch_index.csv records the original size so outputs can becropped back to the true extent.

3. patch_index.csv
Column	Type	Meaning
year	int	Observation year
row, col	int	Patch origin (pixels) in the padded mosaic
cloud_frac	float	Fraction of NaN pixels; patches > 0.10 are excluded
orig_h, orig_w	int	Pre-padding raster size
4. labels_{year}.geojson
FeatureCollection of Polygons drawn in EPSG:4326 (geemap drawing); reprojectedto the raster CRS at rasterization time. All features carry class: 1 (mangrove);non-mangrove is implicit background. Unclear areas are not drawn — they arelogged in the uncertain list and may be excluded from testing.

5. metrics.json (produced by evaluate.py, served by /api/metrics)
{  "status": "final",  "f1": 0.0, "iou": 0.0, "mAP": 0.0,  "threshold": 0.0, "split": "80/20",  "config": { "optimizer": "...", "loss": "...", "input": "...", "output": "..." },  "pr_curve": { "recall": [0.0], "precision": [1.0] },  "confusion": { "TP": 0, "FP": 0, "FN": 0, "TN": 0 }}
6. REST API responses (demo data until integration)
GET /api/annual/{year} → { year, geojson, area_ha, pixels }
GET /api/change/{y1}/{y2} → { y1, y2, geojson (features: gain|loss), gain_ha, loss_ha, stable_mangrove_ha, stable_non_mangrove_ha }
GET /api/stats → { per_year: [{year, area_ha}], per_interval: [{interval, gain_ha, loss_ha}] }
GET /api/metrics → schema in §5
7. Units & constants
1 pixel = 100 m² (10 m grid) · Area(ha) = N / 100 · observation period2019–2024 · fixed scene window Feb 1 – Apr 30 (dry season) every year.
