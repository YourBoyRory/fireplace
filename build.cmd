

pip install -r requirements.txt
pyinstaller --windowed --onefile --name "Fireplace" --icon=assets/icon.ico --add-data "assets/icon-small.png:assets" --add-data "assets/fire.gif:assets" --add-data "openCL_stress.cl:." ./Fireplace.py
