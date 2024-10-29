#!/bin/bash

if [[ "$1" != "--use-system-packages" ]]; then
    python -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt
else
    echo "Using system packages"
fi

pyinstaller --name "fireplace" --add-data "assets/icon-small.png:assets" --add-data "assets/fire.gif:assets" --add-data "openCL_stress.cl:." ./Fireplace.py
