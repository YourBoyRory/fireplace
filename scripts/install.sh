#!/bin/bash

sudo mkdir /opt/fireplace
sudo chown root:root /opt/fireplace
sudo cp ./dist/fireplace/fireplace /opt/fireplace
sudo cp -r ./dist/fireplace/_internal /opt/fireplace

sudo ln -s /opt/fireplace/fireplace /usr/local/bin/fireplace

echo "[Desktop Entry]
Version=1.0
Type=Application
Name=Fireplace
Comment=Warm up your room!
Exec=/opt/fireplace/fireplace %U
Icon=/opt/fireplace/_internal/assets/icon-small.png
Terminal=false
Categories=Utility;Application;
StartupNotify=true" | sudo tee -a /usr/share/applications/fireplace.desktop
