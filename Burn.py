import threading
import psutil
import time
import os
from GifPlayer import GifPlayer
from HardwareInfoLib import HardwareLib
from StressTest import CPUStressTest
from StressTest import GPUStressTest

def runGPUStressTest(hardware_info):
    gpuModel = hardware_info.gpuModel
    gpu = GPUStressTest(gpuModel)
    while gpu.runBlender():
        hardware_info.get_gpu_temp()
        time.sleep(1)

def runCPUStressTest(hardware_info):
    cpu = CPUStressTest()
    while cpu.runBlender():
        hardware_info.get_cpu_temp()
        time.sleep(1)

def killChildrenAndThenSelf():  # Last will and testament 
    pid = os.getpid()
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        print("Killing Worker: ", child)
        child.kill()
    parent.kill()

if __name__ == "__main__":
    hardware_info = HardwareLib()
    gpuModel = hardware_info.gpuModel
    gpuWorker = threading.Thread(target=runGPUStressTest, args=(hardware_info,))
    cpuWorker = threading.Thread(target=runCPUStressTest, args=(hardware_info,))
    gpuWorker.start()
    cpuWorker.start()  
    
    GifPlayer("./assets/fire.gif")
    
    killChildrenAndThenSelf()
