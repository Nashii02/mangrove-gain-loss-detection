# Labeling Guidelines

## Purpose

This document describes the preparation and quality checking of the reference labels used for training and validating the U-Net mangrove segmentation model.

## Target Classes

The study uses two classification classes:

| Value | Class |
|---|---|
| 1 | Mangrove |
| 0 | Non-Mangrove |

The reference mask is represented as a binary classification in which each pixel is assigned to either the mangrove or non-mangrove class.

## Reference Mask Preparation

Reference masks are prepared for the Sentinel-2 image patches used during model development.

Each reference mask corresponds to the spatial extent of its associated image patch. The labels provide the reference information against which the U-Net predictions are compared during training and evaluation.

## Mangrove Label

A pixel is assigned the value:

`1 = Mangrove`

when the reference information identifies the corresponding area as mangrove.

## Non-Mangrove Label

A pixel is assigned the value:

`0 = Non-Mangrove`

when the corresponding area is identified as a non-mangrove area.

## Quality Checking and Validation

The prepared reference masks undergo quality checking before they are used for model training.

The purpose of quality checking is to identify and correct labeling issues that may affect the training and evaluation of the U-Net model.

Reference labels are reviewed to ensure that:

- The mangrove and non-mangrove classes are correctly represented.
- The labels correspond spatially to the associated image patches.
- The binary class values are correctly assigned.
- Incorrect or questionable labels are identified and corrected when necessary.

## Reference Label Workflow

<div align="center">

**Reference Data**

↓

**Reference Mask Preparation**

↓

**Quality Checking**

↓

**Validation and Correction**

↓

**Validated Reference Masks**

↓

**U-Net Model Development**

</div>


## Use in Model Development

The validated reference masks serve as the target labels during U-Net model training.

The model predictions are compared with the reference masks to evaluate how accurately the model identifies mangrove and non-mangrove pixels.

The validated labels are therefore used as the reference basis for model development and subsequent model evaluation.
