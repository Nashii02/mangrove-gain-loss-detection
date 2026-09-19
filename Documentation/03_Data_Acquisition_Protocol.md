# Data Acquisition Protocol

## Purpose

This document describes the procedure used to acquire the Sentinel-2 imagery and reference data required for the mangrove segmentation and multi-temporal change-detection workflow.

## Study Area

The study focuses on **Aringay, La Union**. The study-area boundary is used to define the spatial extent of the satellite imagery to be processed.

## Satellite Imagery

Sentinel-2 satellite imagery covering the study area from **2019 to 2024** is acquired for the study.

The imagery provides the spectral information required for mangrove and non-mangrove classification.

The spectral inputs used in the study are:

- Band 3 (Green)
- Band 4 (Red)
- Band 8 (Near-Infrared)
- Band 11 (Short-Wave Infrared)
- NDVI

## Data Acquisition Process

The data acquisition process consists of the following steps:

1. Define the study-area boundary for Aringay, La Union.
2. Identify Sentinel-2 imagery covering the study area for the period 2019–2024.
3. Select the required Sentinel-2 spectral bands.
4. Prepare the imagery for cloud and cloud-shadow removal.
5. Clip the imagery to the study-area boundary.
6. Organize the imagery according to the corresponding observation year.
7. Prepare the acquired imagery for the succeeding preprocessing stage.

## Required Spectral Data

The following Sentinel-2 bands are used as model inputs:

| Band | Description | Purpose |
|---|---|---|
| B3 | Green | Spectral information for vegetation and surface characterization |
| B4 | Red | Spectral information used for vegetation analysis |
| B8 | Near-Infrared | Vegetation-related spectral information |
| B11 | Short-Wave Infrared | Additional spectral information for land-cover characterization |
| NDVI | Normalized Difference Vegetation Index | Vegetation-related index derived from Red and Near-Infrared information |

## Reference Data

Reference data are also prepared for the creation and validation of mangrove and non-mangrove reference masks.

These reference labels are used during the model-development stage and are subjected to quality checking and validation before training.

## Output of Data Acquisition

The output of this stage consists of:

- Sentinel-2 imagery covering the study area
- Required spectral bands
- Study-area boundary
- Reference data
- Imagery organized according to the 2019–2024 study period

The acquired data are then passed to the **Image Preprocessing** stage.
