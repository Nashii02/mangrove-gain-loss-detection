# User Manual

## System Title

**Deep Learning-Based Detection of Mangrove Gain and Loss in Aringay, La Union**

## Purpose

This user manual provides the basic procedures for using the prototype system to process Sentinel-2 imagery, generate mangrove classification maps, detect mapped mangrove gain and loss, calculate areas, and view the resulting outputs.

## System Workflow

<div align="center">

**Input Sentinel-2 Imagery**

↓

**Image Preprocessing**

↓

**U-Net Mangrove Segmentation**

↓

**Classification Thresholding**

↓

**Annual Mangrove Maps**

↓

**Multi-Temporal Change Detection**

↓

**Area Calculation**

↓

**Maps and Statistical Summaries**

</div>

## 1. Prepare the Input Data

Prepare the required Sentinel-2 imagery covering the study area.

The input imagery should contain the required spectral information:

- Band 3 (Green)
- Band 4 (Red)
- Band 8 (Near-Infrared)
- Band 11 (Short-Wave Infrared)

NDVI is generated as part of the preprocessing procedure.

The imagery should correspond to the study period from **2019 to 2024**.

## 2. Load the Input Imagery

Load the prepared Sentinel-2 imagery into the prototype system.

The system uses the selected imagery as input for the succeeding preprocessing and segmentation procedures.

## 3. Perform Image Preprocessing

The system prepares the imagery before it is passed to the U-Net model.

The preprocessing stage includes the required procedures for:

- Cloud and cloud-shadow removal
- Study-area cropping
- Spatial alignment
- Resampling
- Normalization
- Missing-pixel handling
- NDVI calculation

The resulting input consists of five channels:

`B3 + B4 + B8 + B11 + NDVI`

## 4. Perform Mangrove Segmentation

The preprocessed imagery is passed to the trained U-Net model.

The U-Net model produces a pixel-level probability representing the likelihood that each pixel belongs to the mangrove class.

The probability output is converted into a binary classification using the finalized classification threshold.

The resulting classes are:

| Value | Class |
|---|---|
| 1 | Mangrove |
| 0 | Non-Mangrove |

## 5. Generate Annual Mangrove Maps

The finalized model is applied to the imagery for each year from 2019 to 2024.

The system generates an annual mangrove classification map for each corresponding year.

These maps show the spatial distribution of the mapped mangrove and non-mangrove classes.

## 6. Perform Change Detection

The annual mangrove maps are compared between consecutive years.

The system identifies the following pixel-level transitions:

| Previous Year | Current Year | Classification |
|---|---|---|
| 0 | 1 | Mapped Mangrove Gain |
| 1 | 0 | Mapped Mangrove Loss |
| 1 | 1 | Stable Mangrove |
| 0 | 0 | Stable Non-Mangrove |

## 7. Calculate Mangrove Area

The system calculates the area corresponding to the classified pixels.

For Sentinel-2 imagery with a 10 m spatial resolution:

`10 m × 10 m = 100 m²`

`100 m² = 0.01 hectare`

The area is calculated using:

`Area (hectares) = Number of classified pixels × 0.01`

The calculated values can be used to summarize the mapped mangrove area and mapped changes between years.

## 8. View the Results

The prototype provides outputs that may include:

- Annual mangrove maps
- Mapped mangrove gain areas
- Mapped mangrove loss areas
- Stable mangrove areas
- Stable non-mangrove areas
- Area statistics
- Statistical summaries

The displayed results should correspond to the processed imagery and generated classification outputs.

## 9. Interpretation of Results

The mapped gain and loss results represent changes detected from the classified satellite imagery.

**Mapped Mangrove Gain** refers to pixels classified as non-mangrove in the previous year and mangrove in the current year.

**Mapped Mangrove Loss** refers to pixels classified as mangrove in the previous year and non-mangrove in the current year.

These classifications describe changes in the mapped results and do not by themselves establish the specific environmental or human causes of the changes.

## 10. Basic User Procedure

The basic procedure for using the prototype is:

1. Prepare the Sentinel-2 imagery.
2. Load the required imagery into the system.
3. Run the preprocessing procedure.
4. Run the U-Net segmentation.
5. Apply the finalized classification threshold.
6. Generate the annual mangrove maps.
7. Run the change-detection procedure.
8. Calculate the corresponding areas.
9. View the generated maps and statistical summaries.

## Expected Output

After completing the workflow, the system should provide:

- Classified mangrove maps
- Multi-temporal mapped change results
- Mapped mangrove gain and loss information
- Area calculations
- Maps and statistical summaries
