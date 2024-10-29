
python -m venv ./venv
source ./venv/Scripts/activate.bat
pip install -r requirements.txt
pyinstaller --windowed --onefile --name "Fireplace" --icon=assets/icon.ico --add-data "assets/icon-small.png:assets" --add-data "assets/fire.gif:assets" --add-data "opencl_workloads/opencl_stress.cl:opencl_workloads" ./Fireplace.py
echo.
echo Build Done
echo.
dir ./dist/
