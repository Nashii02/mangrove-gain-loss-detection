runbook

0. Code
git clone https://github.com//mangrove-monitoring-system.gitcd mangrove-monitoring-system

1. Environment
python -m venv venv && source venv/bin/activatepip install -r "Dependencies and Environment/requirements.txt"

2. Web prototype (demo)
cd SourceCode && python app.py # http://127.0.0.1:5000 → Ctrl+C → cd ..

3. Data acquisition + preprocessing (Colab)
open colab_notebooks/01_data_acquisition_and_preprocessing.ipynb → T4 GPU → run all
outputs: Drive/GEE_Exports (TIFs) + Drive/mangrove_project/data (patches, labels)
4. Labeling + MENRO validation (manual)
draw polygons per year → labels_{year}.geojson → rasterize → mask patches
⛔ no training before MENRO sign-off
5. Training + evaluation (notebook 02 — to be added)
produces: final_model.keras + Model/metrics.json
6. Integration
DEMO_MODE = False in app.py → fill >>> INTEGRATION blocks → copy metrics.json to Model/
7. Verify — web system now serves real outputs
cd SourceCode && python app.py

Definition of done
 /maps shows 6 real annual maps
 /change shows 5 real consecutive-year comparisons
 /statistics matches thesis transition table
 /model shows final F1, IoU, mAP + locked threshold
 /report downloads a PDF with real figures
