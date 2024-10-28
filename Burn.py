import threading
import time
from GifPlayer import GifPlayer
from HardwareInfoLib import HardwareLib
from StressTest import CPUStressTest
from StressTest import GPUStressTest

def runGPUStressTest(gpuModel):
    gpu = GPUStressTest(gpuModel)
    while gpu.runBlender():
        time.sleep(1)

def runCPUStressTest():
    cpu = CPUStressTest()
    while cpu.runBlender():
        time.sleep(1)

if __name__ == "__main__":
    hardware_info = HardwareLib()
    gpuWorker = threading.Thread(target=runGPUStressTest, args=hardware_info.gpuModel)
    cpuWorker = threading.Thread(target=runCPUStressTest)
    gpuWorker.start()
    cpuWorker.start()    
    GifPlayer("./assets/fire.gif")
