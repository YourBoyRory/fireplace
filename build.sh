
copyDependency() {
    cp -r ./dist/Burn/_internal_full/$1 ./dist/Burn/_internal/$1
}

pyinstaller --name "Burn" --add-data "assets/fire.gif:assets" --add-data "openCL_stress.cl:." ./Burn.py
if [[ $? -eq 0 ]]; then
    rm ./dist/Burn/_internal_full
    mv ./dist/Burn/_internal ./dist/Burn/_internal_full
    mkdir ./dist/Burn/_internal

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
fi
