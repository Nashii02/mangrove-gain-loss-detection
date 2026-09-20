Colab Notebooks — Run Order
#	Notebook	Status	Purpose
1	01_data_acquisition_and_preprocessing.ipynb	WIP (under revision)	GEE auth → Sentinel-2 export (6 yrs) → verification → 256×256 patches → labeling map
2	02_training_and_evaluation.ipynb	planned	U-Net training (80/20) → F1/IoU/mAP → threshold lock
3	03_change_detection.ipynb	planned	annual maps → transitions → hectares
Collaborator rules

Clear all outputs before committing (auth cells must never contain output)
Keep ROI, YEARS, prep() defined only in the CONFIG cell (single source of truth)
Log selected scene date + MGRS tile per year in a markdown cell (provenance)
