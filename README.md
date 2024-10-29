## Overview
This program runs **Prime Number Generation** on the CPU and **OpenCL Workloads** on the GPU to generate as much heat as possible.
I made this because I was cold, but I guess you could use this for thermal testing.

## Usage
- **Launch**: Run the program.
- **Profit?**: PC gets warm!
- **Hot Enought?**: Press Esc or Close the program

## Command Line Arguments

    --fullscreen    - Launch the fireplace movie in fullscreen, but you can press F11 to fullscreen as well.

## Build From git

****Make sure you have ``python`` and ``pip`` installed***<br>

**Pull git repo**

    git clone https://github.com/YourBoyRory/fireplace.git
<br>

**Run build script for your platform in**

    ./scripts/build-linux.sh
    .\scripts\build-windows.cmd
<br>

**Retrieve binary from ``/dist/``**<br>
- Windows is built to ``/dist/Fireplace.exe``
- Linux is built to ``/dist/fireplace/``
    - ``/dist/fireplace/_internal`` is required on Linux
    - Linux can be installed and uninstalled using the respective scripts located in ``/scripts/`` 
