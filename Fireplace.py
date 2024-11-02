import os
import sys
from GifPlayer import GifPlayer
from StressTest import CPUStressTest
from StressTest import GPUStressTest

def getAssetPath(file):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, 'assets', file)

if __name__ == "__main__":

    gpuStresser = GPUStressTest()
    cpuStresser = CPUStressTest()

    try:
        cpuStresser.startLoad()
        gpuStresser.startLoad()
        GifPlayer(getAssetPath('fire.gif'))
    except Exception as e:
        print(f"\nAh shit, here we go again...\n    Exception: {e}")
    finally:
        print("Info: Starting Shutdown, Goodbye...")
        cpuStresser.stopLoad()
        gpuStresser.stopLoad()
