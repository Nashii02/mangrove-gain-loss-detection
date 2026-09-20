"""
Step 2 — Patch extraction
Tiles each year's 5-band GeoTIFF into 256×256 patches (NaN = cloud/missing),
excluding patches with >10% missing pixels (thesis: "handling missing pixels").
Writes patches + patch_index.csv.  Status: v1 — ported from notebook.
"""
import csv
import numpy as np
import rasterio
from config import DRIVE_DIR, IMAGES_DIR, OUT_DIR, YEARS, PATCH, MAX_CLOUD_FRAC


def pad_to_patch(arr, pad_val=0.0):
    """Pad (H, W, C) so H, W become multiples of PATCH. Returns (padded, (H0, W0))."""
    H, W, C = arr.shape
    Hp = ((H + PATCH - 1) // PATCH) * PATCH
    Wp = ((W + PATCH - 1) // PATCH) * PATCH
    out = np.full((Hp, Wp, C), pad_val, dtype="float32")
    out[:H, :W, :] = arr
    return out, (H, W)


def make_patches():
    index_rows = []
    for year in YEARS:
        tif = DRIVE_DIR / f"DULAO_{year}.tif"
        if not tif.exists():
            print(f"{year}: ⚠ {tif.name} not found — export first"); continue

        with rasterio.open(tif) as src:
            arr = src.read()                          # (5, H, W)
            nodata = ~src.read_masks().astype(bool)   # True = cloud-masked
        arr = np.transpose(arr, (1, 2, 0)).astype("float32")
        arr[nodata.transpose(1, 2, 0)] = np.nan

        arr, (H0, W0) = pad_to_patch(arr, pad_val=np.nan)
        kept = skipped = 0
        for r in range(0, arr.shape[0], PATCH):
            for c in range(0, arr.shape[1], PATCH):
                patch = arr[r:r + PATCH, c:c + PATCH]
                cloud_frac = float(np.isnan(patch).mean())
                if cloud_frac > MAX_CLOUD_FRAC:
                    skipped += 1
                    continue
                patch = np.nan_to_num(patch, nan=0.0)
                np.save(IMAGES_DIR / f"{year}_{r:04d}_{c:04d}.npy", patch)
                index_rows.append([year, r, c, round(cloud_frac, 4), H0, W0])
                kept += 1
        print(f"{year}: image {H0}x{W0} | kept {kept}, skipped {skipped}")

    with open(OUT_DIR / "patch_index.csv", "w", newline="") as f:
        csv.writer(f).writerows(
            [["year", "row", "col", "cloud_frac", "orig_h", "orig_w"], *index_rows])
    print(f"\nTotal image patches: {len(index_rows)}")


if __name__ == "__main__":
    make_patches()
