"""
Step 1 — Data Acquisition
Selects the least-cloudy same-season Sentinel-2 L2A scene per year (2019–2024),
applies cloud masking + band scaling + B11 bilinear resampling (20 m → 10 m) +
NDVI, and queues a 5-band GeoTIFF export to Google Drive.

Run on Colab after `ee.Authenticate()`.  Status: v1 — ported from notebook.
"""
import ee
from config import (PROJECT_ID, COLLECTION, MAX_CLOUD, BAND_SCALE,
                    YEARS, START, END, get_roi)

ee.Initialize(project=PROJECT_ID)
ROI = get_roi(ee)


def prep(img):
    """One scene → masked, scaled, resampled, NDVI-added 5-band image."""
    # 1) mask clouds / shadows / cirrus via the Scene Classification Layer
    scl = img.select("SCL")
    bad = scl.eq(3).Or(scl.eq(8)).Or(scl.eq(9)).Or(scl.eq(10))
    img = img.updateMask(bad.Not())

    # 2) scale 10 m bands to reflectance 0–1
    b3 = img.select("B3").divide(BAND_SCALE)
    b4 = img.select("B4").divide(BAND_SCALE)
    b8 = img.select("B8").divide(BAND_SCALE)

    # 3) B11 native 20 m → bilinear resample to the 10 m grid (thesis spec)
    b11 = img.select("B11").resample("bilinear").divide(BAND_SCALE)

    # 4) NDVI rescaled to 0–1 so all five layers share one value range
    ndvi = (b8.subtract(b4).divide(b8.add(b4))
              .multiply(0.5).add(0.5).rename("NDVI"))

    return b3.addBands([b4, b8, b11, ndvi])       # B3, B4, B8, B11, NDVI


def select_scene(year):
    """Same selection logic used by the labeling map → what you see == what you get."""
    return (ee.ImageCollection(COLLECTION)
            .filterBounds(ROI)
            .filterDate(f"{year}{START}", f"{year}{END}")
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD))
            .sort("CLOUDY_PIXEL_PERCENTAGE"))


def export_year(year):
    col = select_scene(year)
    if col.size().getInfo() == 0:
        print(f"{year}: ⚠ no scenes — widen the date window and rerun")
        return
    img  = ee.Image(col.first())
    date = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd").getInfo()
    crs  = img.select("B3").projection().getInfo()["crs"]
    tile = img.get("MGRS_TILE").getInfo()
    print(f"{year}: {col.size().getInfo()} scenes | using {date} | tile {tile} | crs {crs}")

    ee.batch.Export.image.toDrive(
        image=prep(img).clip(ROI).toFloat(),
        description=f"DULAO_{year}",
        folder="GEE_Exports",
        region=ROI, scale=10, crs=crs, maxPixels=1e13,
    ).start()


if __name__ == "__main__":
    for y in YEARS:
        export_year(y)
    print("\nAll tasks queued — monitor with:  [t.status()['state'] for t in ee.batch.Task.list()]")
