import math
import os
import sys
import multiprocessing
import pyopencl as cl
import numpy as np

class CPUStressTest:
    def __isPrime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def __generatePrimes(self):
        num = 2
        while True:
            if self.__isPrime(num):
                pass
            num += 1

    def startLoad(self):
        self.num_workers = multiprocessing.cpu_count()
        # this makes make sure there are cores avalible so the system is usable
        if self.num_workers > 2:
            self.num_workers -= 2
        else:
            self.num_workers -= 1

        print(f"CPU Info: Dispatching {self.num_workers} CPU Worker")

        self.__workers = []
        for _ in range(self.num_workers):
            worker = multiprocessing.Process(target=self.__generatePrimes)
            self.__workers.append(worker)
            worker.start()
            print("    Started CPU Worker")

    def stopLoad(self):
        print(f"CPU Info: Stopping {self.num_workers} CPU Worker")
        for worker in self.__workers:
            worker.terminate()
            print("    Stopped CPU Worker")
        print(f"CPU Info: Stopped CPU Dispatcher")
        for worker in self.__workers:
            worker.join()

class GPUStressTest:

    def __run(self):
        context, queue = self.__create_context_and_queue()

        # 50 MB buffer
        size = 50 * 1024 * 1024
        data = np.random.rand(size).astype(np.float32)
        mf = cl.mem_flags
        data_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=data)

        program = self.__compile_openCL(context, "openCL_stress.cl")
        print("GPU Info: Started GPU Worker")
        while True:
            global_size = (size,)
            program.load_gpu(queue, global_size, None, data_buf)
            queue.finish()

    def __compile_openCL(self, context, clFile):
        print("GPU Info: Compiling OpenCL workload.")
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        clFile_full_path = os.path.join(base_path, clFile)
        with open(clFile_full_path, 'r') as f:
            kernel_code = f.read()
        program = cl.Program(context, kernel_code).build()
        print("GPU Info: Compilation done")
        return program

    def __create_context_and_queue(self):
        platforms = cl.get_platforms()
        context = cl.Context([platforms[1].get_devices()[0]])
        queue = cl.CommandQueue(context)
        return context, queue

    def startLoad(self):
        self.worker = multiprocessing.Process(target=self.__run)
        self.worker.start()
        print("GPU Info: Dispatching GPU Worker")

    def stopLoad(self):
        if self.worker:
            self.worker.terminate()
            self.worker.join()
            self.worker = None
        print("GPU Info: Stopped GPU Worker")

