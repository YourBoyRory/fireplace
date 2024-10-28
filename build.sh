
copyDependency() {
    cp -r ./dist/fireplace/_internal_full/$1 ./dist/fireplace/_internal/$1
}

pip install -r requirements.txt

pyinstaller --name "fireplace" --add-data "assets/fire.gif:assets" --add-data "openCL_stress.cl:." ./Fireplace.py
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
    tar -czvf ../fireplace.tar.gz _internal fireplace
    echo "files in dist"
fi
