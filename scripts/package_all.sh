#!/bin/bash


copyDependency() {
    cp -r ./_internal_full/$1 ./_internal/$1
}

echo "Build and packaging for Linux"
./build-linux.sh --use-system-packages
if [[ $? -eq 0 ]]; then
    cd ../dist/fireplace
    rm ./_internal_full
    mv ./_internal ./_internal_full
    mkdir ./_internal

    #files
    copyDependency "assets"
    copyDependency "openCL_stress.cl"

    # Libs
    copyDependency "setuptools"
    copyDependency "lib-dynload"
    copyDependency "numpy"
    copyDependency "jaraco"
    copyDependency "pyopencl"
    copyDependency "pyopencl-2024.2.6.dist-info"
    copyDependency "libscipy_openblas64_-ff651d7f.so"
    copyDependency "PyQt5"

    # Python
    copyDependency "base_library.zip"
    copyDependency "libpython3.12.so.1.0"

    tar -czvf ../fireplace-linux.tar.gz _internal fireplace
    cd ../../scripts/
fi

echo "Build and packaging for Windows"
wine ./build-windows.cmd
cd ../dist/
zip  ./fireplace-windows.zip ./Fireplace.exe

echo " "
echo "Packaging Complete"
echo " "
cd ..
ls -lh ./dist/fireplace-windows.zip 
ls -lh ./dist/fireplace-linux.tar.gz
