
Model Card — U-Net Mangrove Segmentation
Status: training not yet conducted — metrics will be reported after thefinal training run, following revision of the pipeline scripts.

Item	Value
Model	U-Net encoder–decoder CNN with skip connections (Ronneberger et al., 2015), adapted for 5-channel Sentinel-2 input
Task	Pixel-level binary semantic segmentation — mangrove (1) vs. non-mangrove (0)
Input	256×256×5 patch — Sentinel-2 B3 (Green), B4 (Red), B8 (NIR), B11 (SWIR, bilinear-resampled 20 m → 10 m), NDVI — reflectance 0–1
Output	256×256×1 sigmoid probability map → binary mask at the locked classification threshold
Intended use
Automated detection and quantification of mangrove gain and loss in Brgy. Dulao,Aringay, La Union (2019–2024), in support of the Aringay MENRO's environmentalmonitoring and conservation planning. Prototype stage — outputinterpretability, not operationalization.

Training configuration (planned, per thesis)
Item	Value
Optimizer / learning rate	Adam / 0.001
Loss	Binary cross-entropy
Data split	80% training / 20% validation
Overfitting control	Train vs. validation loss monitoring; early stopping; batch size, epochs, augmentation, class-imbalance handling and stopping criteria recorded
Threshold selection	Threshold sweep 0.05–0.95 (step 0.05); operating threshold = maximum validation IoU, then locked with the final model
Evaluation (to be conducted)
Metric	Result
F1-score	will be reported
Intersection over Union (IoU)	will be reported
mean Average Precision (mAP)	will be reported — equals the AP of the mangrove class (single positive class)
Operating threshold (locked)	will be reported
Baseline protocol: the performance of the first trained model will serve asthe baseline; subsequent iterations will be assessed against it as astudy-specific evaluation method rather than a universal acceptance threshold.Reference-label adjustments will follow the established labeling procedure andwill not be made solely for performance reasons.

Limitations (anticipated)
The study will not create a truly independent test dataset; validationresults will be treated as estimates for the study's reference-data conditions.
10 m spatial resolution may limit detection of very small or narrow mangrovefragments.
Mapped transitions will be interpreted as probable land-cover changes, notconfirmed ecological causes; interpretation requires supporting local records.
Reference labels will be researcher-prepared and independently validated byAringay MENRO core officers (single-validator expert review).
