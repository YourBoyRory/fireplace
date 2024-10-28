import subprocess
import random
import time
blender_cli = "./bin/benchmark-launcher-cli"
blender_version = "4.2.0"
blender_render_list = ["classroom", "monster", "junkshop"]

class CPUStressTest:
    def runBlender(self):
        random.shuffle(blender_render_list)
        for render in blender_render_list:
            subprocess.run([blender_cli, "benchmark", render, "--blender-version", blender_version, "--device-type", "CPU"])
        return True

class GPUStressTest:
    
    def __init__(self, gpuModel):
        self.GAPI = self.getGraphicsAPI(gpuModel)
    
    def runBlender(self):
        if self.GAPI != None:
            random.shuffle(blender_render_list)
            for render in blender_render_list:
                subprocess.run([blender_cli, "benchmark", render, "--blender-version", blender_version, "--device-type", self.GAPI])
            return True
        else:
            print("ERROR: GPU not supported. Locking GPU thread.")
            return False

    def getGraphicsAPI(self, gpuModel):
        if gpuModel == "Nvidia":
            return "CUDA"
        elif gpuModel == "AMD":
            return "HIP"
        elif gpuModel == "Intel":
            return "ONEAPI"
        else:
            return None
    
