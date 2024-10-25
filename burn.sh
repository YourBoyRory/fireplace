burn() {
    while true; do
        ./bin/benchmark-launcher-cli benchmark classroom --blender-version 4.2.0 --device-type $1
        sleep 1
    done
}

displayGif() {
    pqiv --hide-info-box --fullscreen --scale-images-up ./assets/fire.gif
    killall blender 
    killall bash
}

burn CPU &
burn CUDA &
displayGif

