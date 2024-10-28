import math
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
        num_workers = multiprocessing.cpu_count()
        if num_workers > 2:
            num_workers -= 2
        else:
            num_workers -= 1

        self.__workers = []
        for _ in range(num_workers):
            worker = multiprocessing.Process(target=self.__generatePrimes)
            self.__workers.append(worker)
            worker.start()

    def stopLoad(self):
        for worker in self.__workers:
            worker.terminate()
        for worker in self.__workers:
            worker.join()

class GPUStressTest:

    def __run(self):
        # Set up OpenCL context and queue
        context, queue = self.__create_context_and_queue()

        # Create a very large buffer
        size = 50 * 1024 * 1024  # 50 MB of data to stress the GPU
        data = np.random.rand(size).astype(np.float32)
        mf = cl.mem_flags
        data_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=data)

        # Compile the kernel
        with open('openCL_stress.cl', 'r') as f:
            kernel_code = f.read()
        program = cl.Program(context, kernel_code).build()

        # Infinite loop to keep GPU busy
        while True:
            # Launch a large number of work items
            global_size = (size,)  # Adjust as necessary
            program.load_gpu(queue, global_size, None, data_buf)
            queue.finish()

    def __create_context_and_queue(self):
        platforms = cl.get_platforms()
        context = cl.Context([platforms[1].get_devices()[0]])
        queue = cl.CommandQueue(context)
        return context, queue

    def startLoad(self):
        self.process = multiprocessing.Process(target=self.__run)
        self.process.start()

    def stopLoad(self):
        if self.process:
            self.process.terminate()
            self.process.join()
            self.process = None

