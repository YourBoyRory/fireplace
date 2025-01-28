
python -m venv ./venv-windows
source ./venv-windows/Scripts/activate.bat
pip install -r requirements-windows.txt
pyinstaller --windowed --name "Fireplace" --icon=assets/icon.ico --add-data "assets/font.ttf:assets" --add-data "lib/OpenHardwareMonitorLib.sys:lib" --add-data "lib/OpenHardwareMonitorLib.dll:lib" --add-data "assets/icon-small.png:assets" --add-data "assets/fire.gif:assets" --add-data "opencl_workloads/opencl_stress.cl:opencl_workloads" ./Fireplace.py
echo.
echo Build Done
echo.
dir ./dist/
