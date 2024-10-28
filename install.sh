#!/bin/bash

sudo mkdir /opt/burn
sudo chown root:root /opt/burn
sudo cp ./dist/Burn/Burn /opt/burn
sudo cp -r ./dist/Burn/_internal /opt/burn
