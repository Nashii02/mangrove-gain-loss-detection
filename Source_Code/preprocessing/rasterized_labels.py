"""
Step 3 — Reference labels → binary masks
Reads labels_{year}.geojson (drawn in EPSG:4326), REPROJECTS to the raster CRS
(critical fix — drawn coordinates are lon/lat, rasters are UTM meters), rasterizes
mangrove = 1 / non-mangrove = 0, writes MASK_{year}.tif and aligned mask patches.

Status: v1 — ported from notebook (includes the CRS reprojection fix).
"""
import json
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from config import DRIVE_DIR, IMAGES_DIR, MASKS_DIR, LABELS_DIR, OUT_DIR, YEARS, PATCH


def make_mask(year):
    lab = LABELS_DIR / f"labels_{year}.geojson"
    if not lab.exists():
        print(f"⚠ {year}: no label file yet — skipping"); return

    gdf = gpd.read_file(lab)                       # drawn in lon/lat (EPSG:4326)
    if len(gdf) == 0:
        print(f"⚠ {year}: label file is empty"); return

    with rasterio.open(DRIVE_DIR / f"DULAO_{year}.tif") as src:
        gdf = gdf.to_crs(src.crs)                  # ← THE FIX: lon/lat → raster CRS
        mask = rasterize(gdf.geometry, out_shape=src.shape,
                         transform=src.transform, fill=0,
                         default_value=1, dtype="uint8")     # 1 = mangrove
        prof = src.profile.copy()
        prof.update(count=1, dtype="uint8", nodata=255)
    with rasterio.open(OUT_DIR / f"MASK_{year}.tif", "w", **prof) as dst:
        dst.write(mask, 1)

    m, _ = np.asarray([mask.astype("float32")]), None
    H, W = mask.shape
    Hp = ((H + PATCH - 1) // PATCH) * PATCH
    Wp = ((W + PATCH - 1) // PATCH) * PATCH
    padded = np.zeros((Hp, Wp), dtype="float32")
    padded[:H, :W] = mask                          # same padding as image patches

    n = 0
    for r in range(0, Hp, PATCH):
        for c in range(0, Wp, PATCH):
            img_p = IMAGES_DIR / f"{year}_{r:04d}_{c:04d}.npy"
            if img_p.exists():                     # only patches kept in step 2
                np.save(MASKS_DIR / f"{year}_{r:04d}_{c:04d}.npy",
                        padded[r:r + PATCH, c:c + PATCH])
                n += 1
    print(f"{year}: mangrove px = {int(mask.sum())} | mask patches = {n}")


if __name__ == "__main__":
    for y in YEARS:
        make_mask(y)
