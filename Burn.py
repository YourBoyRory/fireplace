import os
import sys
from GifPlayer import GifPlayer
from StressTest import CPUStressTest
from StressTest import GPUStressTest

gpuStresser = GPUStressTest()
cpuStresser = CPUStressTest()

def startTests():
    cpuStresser.startLoad()
    gpuStresser.startLoad()

def stopTests():
    cpuStresser.stopLoad()
    gpuStresser.stopLoad()

def getAssetPath(file):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, 'assets', file)

if __name__ == "__main__":
    startTests()
    GifPlayer(getAssetPath('fire.gif'))
    stopTests()
