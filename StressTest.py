import math
import os
import sys
import time
import multiprocessing
import pyopencl as cl
import numpy as np

class CPUStressTest:
    def isPrime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generatePrimes(self):
        num = 2
        while True:
            if self.isPrime(num):
                pass
            num += 1

    def startLoad(self):
        multiprocessing.freeze_support()
        num_workers = multiprocessing.cpu_count()
        # this makes make sure there are cores avalible so the system is usable
        if num_workers > 2:
            num_workers -= 2
        else:
            num_workers -= 1

        print(f"CPU Info: Dispatching {num_workers} CPU Worker")

        workers = []
        for _ in range(num_workers):
            worker = multiprocessing.Process(target=self.generatePrimes)
            workers.append(worker)
            worker.start()
            print("    Started CPU Worker")
        self.workers = workers

    def stopLoad(self):
        print(f"CPU Info: Stopping {len(self.workers)} CPU Worker")
        for worker in self.workers:
            worker.terminate()
            print("    Stopped CPU Worker")
        print(f"CPU Info: Stopped CPU Dispatcher")
        for worker in self.workers:
            worker.join()

class GPUStressTest:

    def run(self):
        context, queue = self.create_context_and_queue()

        # 50 MB buffer
        size = 50 * 1024 * 1024
        data = np.random.rand(size).astype(np.float32)
        mf = cl.mem_flags
        data_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=data)

        program = self.compile_openCL(context, "opencl_stress.cl")
        print("GPU Info: Started GPU Worker")
        while True:
            global_size = (size,)
            program.load_gpu(queue, global_size, None, data_buf)
            queue.finish()

    def compile_openCL(self, context, clFile):
        print("GPU Info: Compiling OpenCL workload.")
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        clFile_full_path = os.path.join(base_path, 'opencl_workloads', clFile)
        with open(clFile_full_path, 'r') as f:
            kernel_code = f.read()
        program = cl.Program(context, kernel_code).build()
        print("GPU Info: Compilation done")
        return program

    def create_context_and_queue(self):
        device = self.getWorker()
        context = cl.Context([device])
        queue = cl.CommandQueue(context)
        return context, queue

    def getWorker(self):
        platforms = cl.get_platforms()
        nvidia_device = None
        amd_device = None
        intel_device = None
        device = None
        # Find first NVIDIA GPU
        for platform in platforms:
            if platform.get_devices() != []:
                if "NVIDIA" in platform.get_devices()[0].name and nvidia_device == None:
                    print("GPU Info: Found NVIDIA device", platform.get_devices()[0].name)
                    nvidia_device = platform.get_devices()[0]
                    break
                elif "AMD" in platform.get_devices()[0].name and amd_device == None:
                    print("GPU Info: Found AMD device", platform.get_devices()[0].name)
                    #amd_device = platform.get_devices()[0]
                    # this is a patch to make it work on my amd desktop, should still works as long as intel igpu is not present too.
                elif "Intel" in platform.get_devices()[0].name and intel_device == None:
                    print("GPU Info: Found Intel device", platform.get_devices()[0].name)
                    intel_device = platform.get_devices()[0]
                elif device == None:
                    print("GPU Info: Found fallback device", platform.get_devices()[0].name)
                    device = platform.get_devices()[0]
        if nvidia_device != None:
            print("GPU Info: Using Nvidia device")
            device = nvidia_device
        elif amd_device != None:
            print("GPU Info: Using AMD device")
            device = amd_device
        elif intel_device != None:
            print("GPU Info: Using Intel device")
            device = intel_device
        else:
            print("Using fallback device")
        print(f"GPU Info: Dispatching GPU Worker on {device}")
        return device

    def startLoad(self):
        multiprocessing.freeze_support()
        worker = multiprocessing.Process(target=self.run)
        worker.start()
        self.worker = worker

    def stopLoad(self):
        if self.worker:
            self.worker.terminate()
            self.worker.join()
            self.worker = None
        print("GPU Info: Stopped GPU Worker")

if __name__ == "__main__":

    gpuStresser = GPUStressTest()
    cpuStresser = CPUStressTest()

    try:
        cpuStresser.startLoad()
        gpuStresser.startLoad()
        input("")
    except Exception as e:
        print(f"\nAh shit, here we go again...\n    Exception: {e}")
    finally:
        print("Info: Starting Shutdown, Goodbye...")
        cpuStresser.stopLoad()
        gpuStresser.stopLoad()
