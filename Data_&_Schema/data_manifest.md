Data Manifest — what exists, where, and why it's not in Git
Large binaries are excluded via .gitignore and live in Google Drive.Update this file whenever an artifact is created or moved.

Artifact	Location	Size (est.)	In Git?
Study-area boundary	repo Data and Schema/samples/study_area_boundary.geojson	2 KB	✅ Yes
5-band annual GeoTIFFs	Drive MyDrive/GEE_Exports/DULAO_{2019..2024}.tif	~1–10 MB each	❌ Drive
Image patches (npy)	Drive MyDrive/mangrove_project/data/images/	—	❌ Drive
Mask patches (npy)	Drive MyDrive/mangrove_project/data/masks/	—	❌ Drive
Label GeoJSONs	Drive .../data/labels/labels_{year}.geojson	KB	❌ Drive (small sample in repo)
Patch index CSV	Drive .../data/patch_index.csv	KB	❌ Drive (sample in repo)
Trained weights	Drive MyDrive/mangrove_project/models/	~200–350 MB	❌ Drive (pointer in Model/weights)
metrics.json (real)	repo Model/metrics.json	KB	✅ Yes — after training
Scene provenance (fill per year as exports run)
Year	Scenes in window	Scene used	MGRS tile	CRS
2019	34	2019-03-27	51QTU	EPSG:32651
2020	—	—	—	—
2021	—	—	—	—
2022	—	—	—	—
2023	—	—	—	—
2024	—	—	—	—
Scene window: Feb 1 – Apr 30 (fixed dry season, identical every year);selection = least-cloudy scene (CLOUDY_PIXEL_PERCENTAGE < 20).
