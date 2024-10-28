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

if __name__ == "__main__":
    startTests()
    GifPlayer("./assets/fire.gif")
    stopTests()
