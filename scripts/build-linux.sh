#!/bin/bash

if [[ "$1" != "--use-system-packages" ]]; then
    python -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt
else
    echo "Using system packages"
fi

pyinstaller --name "fireplace" --add-data "assets/icon-small.png:assets" --add-data "assets/fire.gif:assets" --add-data "opencl_workloads/opencl_stress.cl:opencl_workloads" ./Fireplace.py

echo " "
echo "Packaging Complete"
echo " "

ls -lh ./dist/fireplace
