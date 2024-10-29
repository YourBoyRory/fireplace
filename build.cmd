

pip install -r requirements.txt
pyinstaller --windowed --onefile --name "fireplace" --add-data "assets/fire.gif:assets" --add-data "openCL_stress.cl:." ./Fireplace.py
