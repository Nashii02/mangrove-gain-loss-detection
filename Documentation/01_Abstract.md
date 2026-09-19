# Abstract

Mangrove ecosystems play an important role in protecting coastal areas, supporting biodiversity, and maintaining environmental balance. However, changes in mangrove areas caused by natural and human activities may affect their ecological functions and sustainability.

This study aims to develop a deep learning-based image processing system for detecting and quantifying mapped mangrove gain and loss in Aringay, La Union. The study utilizes Sentinel-2 satellite imagery from 2019 to 2024 and the U-Net deep learning architecture for pixel-level mangrove segmentation. The model uses Bands 3, 4, 8, and 11 together with the Normalized Difference Vegetation Index (NDVI) as input features.

The prepared imagery is organized into 256 × 256 pixel patches and paired with binary reference masks representing mangrove and non-mangrove areas. The U-Net model is trained using the prepared image patches and validated reference labels. Model performance is evaluated using Intersection over Union (IoU), F1-score, and mean Average Precision (mAP). Classification thresholds ranging from 0.05 to 0.95 are evaluated to determine the appropriate threshold for the finalized model.

The finalized model is then applied to the 2019–2024 imagery to generate annual mangrove maps. Consecutive-year maps are compared to identify mapped mangrove gain, mapped mangrove loss, stable mangrove, and stable non-mangrove areas. The corresponding areas are also calculated.

The finalized model and change-detection workflow are integrated into a prototype system intended to support mangrove monitoring and provide maps, change information, area statistics, and summaries for environmental management and conservation activities in Aringay, La Union.
