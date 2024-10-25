touch /tmp/doBurn

burn() {
    while ls /tmp/doBurn; do
        ./bin/benchmark-launcher-cli benchmark classroom --blender-version 4.2.0 --device-type $1
    done
}

list_descendants () {
  local children=$(ps -o pid= --ppid "$1")

  for pid in $children
  do
    list_descendants "$pid"
  done

  echo "$children"
}

displayGif() {
    ./bin/GIF-Player ./assets/fire.gif
    rm /tmp/doBurn
    kill $(list_descendants $$)
}

burn CPU &
burn CUDA &
displayGif

