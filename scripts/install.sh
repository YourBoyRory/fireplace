#!/bin/bash

cd ..

sudo mkdir /opt/fireplace
sudo chown root:root /opt/fireplace
sudo cp ./dist/fireplace/fireplace /opt/fireplace
sudo cp -r ./dist/fireplace/_internal /opt/fireplace

sudo ln -s /opt/fireplace/fireplace /usr/local/bin/fireplace

