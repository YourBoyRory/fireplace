
copyDependency() {
    cp -r ./dist/fireplace/_internal_full/$1 ./dist/fireplace/_internal/$1
}

echo "Build and packaging for Linux"
pip install -r requirements.txt
pyinstaller --name "fireplace" --add-data "assets/icon-small.png:assets" --add-data "assets/fire.gif:assets" --add-data "openCL_stress.cl:." ./Fireplace.py
if [[ $? -eq 0 ]]; then
    rm ./dist/fireplace/_internal_full
    mv ./dist/fireplace/_internal ./dist/fireplace/_internal_full
    mkdir ./dist/fireplace/_internal

    #files
    copyDependency "assets"
    copyDependency "openCL_stress.cl"

    # Libs
    copyDependency "jaraco"
    copyDependency "lib-dynload"
    copyDependency "numpy"
    copyDependency "pyopencl"
    copyDependency "pyopencl-2024.2.6.dist-info"
    copyDependency "PyQt5"

    # Python
    copyDependency "base_library.zip"
    copyDependency "libpython3.12.so.1.0"

    cd ./dist/fireplace
    tar -czvf ../fireplace-linux.tar.gz _internal fireplace
fi

cd ../..
echo "Build and packaging for Windows"
wine ./build-windows.cmd
cd ./dist/
zip  ./fireplace-windows.zip ./Fireplace.exe

echo " "
echo "Packaging Complete"
echo " "
cd ..
ls -lh ./dist/fireplace-windows.zip 
ls -lh ./dist/fireplace-linux.tar.gz
