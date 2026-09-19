# Methodology Summary

## Project

**Deep Learning-Based Detection of Mangrove Gain and Loss in Aringay, La Union**

## Overview

The study follows a sequential workflow consisting of data acquisition, image preprocessing, reference label preparation, U-Net model development, model validation and refinement, multi-temporal change detection, and prototype system implementation and evaluation.

## Research Workflow

**Data Acquisition**  
↓  
**Image Preprocessing**  
↓  
**Reference Label Preparation**  
↓  
**Model Development**  
↓  
**Model Validation and Refinement**  
↓  
**Multi-Temporal Change Detection**  
↓  
**Prototype System Implementation**  
↓  
**Prototype System Evaluation**


## 1. Data Acquisition
Sentinel-2 satellite imagery covering the study area from 2019 to 2024 is collected together with the study-area boundary and necessary reference data.
The primary spectral inputs used in the study are:
- Band 3 (Green)
- Band 4 (Red)
- Band 8 (Near-Infrared)
- Band 11 (Short-Wave Infrared)
- NDVI

## 2. Image Preprocessing
The collected Sentinel-2 imagery is prepared before model training.
The preprocessing procedures include:
- Cloud and cloud-shadow removal
- Cropping to the study area
- Spatial alignment
- Resampling
- Normalization
- Missing-pixel handling
- NDVI calculation
The resulting five-channel inputs consist of:
B3 + B4 + B8 + B11 + NDVI
The processed imagery is then organized into 256 × 256 pixel patches for model development.

## 3. Reference Label Preparation
Reference masks are prepared to represent the target classes:
|    Value    |    Class   |
|-------------|------------| 
|      1      |  Mangrove  |
|      0      |Non-Mangrove|

The reference labels undergo quality checking and validation before being used for model training.

## 4. Model Development
The study uses the U-Net architecture for pixel-level binary semantic segmentation.
The model receives five-channel Sentinel-2 image patches as input:
- B3
- B4
- B8
- B11
- NDVI
The model produces a pixel-level probability output representing the likelihood that each pixel belongs to the mangrove class.
The probability output is converted into a binary classification using a classification threshold:
- Probability ≥ threshold → Mangrove (1)
- Probability < threshold → Non-Mangrove (0)
The model is trained using the prepared image patches and corresponding reference masks.

## 5. Model Validation and Refinement
The trained model is evaluated using:
- **Intersection over Union (IoU)**
- **F1-score**
- **mean Average Precision (mAP)**
Classification thresholds from **0.05 to 0.95** are tested to examine model performance under different probability thresholds.
If refinement is necessary, the workflow returns to the appropriate stage among:

Reference Label Preparation
        ↓
Model Development
        ↓
Model Validation

The model is retrained and re-evaluated when required.
Once the final model configuration and classification threshold are selected, the model is finalized and locked for the succeeding change-detection stage.

## 6. Multi-Temporal Change Detection
The finalized U-Net model and classification threshold are applied consistently to the Sentinel-2 imagery from 2019 to 2024.
Annual mangrove classification maps are generated and consecutive years are compared.
Pixel-level transitions are categorized as:

| Previous Year |  Current Year |    Classification   |
|---------------|---------------|---------------------|
|      0        |      1        | Mapped Mangrove Gain|
|      1        |      0        | Mapped Mangrove Loss|
|      1        |      1        |   Stable Mangrove   |
|      0        |      0        | Stable Non-Mangrove |

The corresponding areas of the classified categories are calculated.
For the 10 m spatial resolution:
10 m × 10 m = 100 m²
100 m² = 0.01 hectare
Therefore:
Area (hectares) = Number of classified pixels / 100

## 7. Prototype System Implementation
The finalized components are integrated into the prototype system.
The prototype incorporates:
- Sentinel-2 image preprocessing
- U-Net-based mangrove segmentation
- Classification thresholding
- Annual mangrove-map generation
- Multi-temporal change detection
- Area computation
- Map visualization
- Statistical summaries

## 8. Prototype System Evaluation
The prototype is evaluated based on its ability to:
1. Accept prepared Sentinel-2 imagery.
2. Perform the required preprocessing.
3. Perform mangrove and non-mangrove segmentation.
4. Generate annual mangrove maps.
5. Identify mapped mangrove gain and loss.
6. Calculate corresponding areas.
7. Display maps and summaries correctly.

## Summary

The methodology establishes a workflow in which the Sentinel-2 imagery is prepared, reference labels are validated, and the U-Net model is trained and evaluated before being used for multi-temporal change detection.

After the final model configuration and classification threshold are selected, the finalized model is applied to the 2019–2024 imagery. The resulting annual mangrove maps are compared between consecutive years to identify mapped mangrove gain, mapped mangrove loss, stable mangrove, and stable non-mangrove areas.

The resulting maps, change-detection outputs, area calculations, and summaries are then integrated into the prototype system for evaluation.
