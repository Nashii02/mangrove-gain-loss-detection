Setup Guide
Path	Who	Purpose	Time
A	Everyone	Run the web prototype	5 min
B	ML pipeline	Colab training environment	10 min
C	Local dev	Jupyter on own PC	15–30 min
D	Data acquisition	Google Earth Engine access	one-time
Path A — Web prototype
git clone https://github.com/<org>/mangrove-monitoring-system.gitcd mangrove-monitoring-systempython -m venv venvsource venv/bin/activate            # Windows: venv\Scripts\activatepip install -r "Dependencies and Environment/requirements.txt"cd SourceCode && python app.py      # → http://127.0.0.1:5000
Runs on demo data. Integration points: search >>> INTEGRATION in app.py.(Frontend-only review needs just: pip install flask reportlab numpy.)

Path B — Google Colab (recommended for the ML pipeline)
Open colab_notebooks/01_data_acquisition_and_preprocessing.ipynb
Runtime → Change runtime type → T4 GPU
Run cells top-to-bottom; Drive mounts automatically
Path C — Local Jupyter
conda env create -f "Dependencies and Environment/environment.yml"conda activate mangrovejupyter lab
NVIDIA GPU recommended for training; CPU fine for preprocessing/inference.

Path D — Google Earth Engine (one-time)
Register at https://code.earthengine.google.com → Noncommercial (instant, free)
Create a Cloud Project; copy the project ID (like ee-yourname — ID, not display name)
Authenticate:
import eeee.Authenticate()                        # same Google account that owns the projectee.Initialize(project="ee-yourname")     # paste YOUR project IDprint(ee.Number(1).getInfo())            # must print 1
Common errors
Error	Fix
Please authorize access...	rerun ee.Authenticate()
not registered for Earth Engine	finish registration in the Code Editor
Invalid project ID	used name, not ID
pip fails on rasterio (Windows)	use conda (Path C)
Blank plots / NaN stats	cloud pixels are NaN — use NaN-safe stretch in notebook
TensorFlow won't import (Py 3.13)	use Python 3.10 or Colab
