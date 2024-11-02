import platform

class LinuxHardwareLib:

    def __init__(self):
        
        import subprocess
        import psutil
        self.driver = "Linux"
        
        if self.__get_nvidia_gpu_temp():
            self.gpuModel = "Nvidia"
        elif self.__get_amd_gpu_temp():
            self.gpuModel = "AMD"
        elif self.__get_intel_gpu_temp():
            self.gpuModel = "Intel"
        else:
            self.gpuModel = None
        try:
            temperatures = psutil.sensors_temperatures()
            temp = temperatures['coretemp'][0][1]
            self.cpuModel = "Intel"
        except:
            try:
                temperatures = psutil.sensors_temperatures()
                temp = temperatures['k10temp'][0][1]
                self.cpuModel = "AMD"
            except:
                self.cpuModel = None
        print(f"Hardware Info: Platform established as {self.driver} running on {self.cpuModel} CPU with {self.gpuModel} GPU")
        
    def __get_nvidia_gpu_temp(self):
        import subprocess
        try:
            result = subprocess.run(['/usr/bin/nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            temp = result.stdout.decode('utf-8').strip()
            return int(temp)
        except:
           return None

    def __get_nvidia_gpu_usage(self):
        import subprocess
        try:
            result = subprocess.run(['/usr/bin/nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            usage = result.stdout.decode('utf-8').strip()
            return int(usage)
        except:
            return None

    def __get_amd_gpu_temp(self):
        import subprocess
        try:
            result = subprocess.run(['/opt/rocm/bin/rocm-smi', '--showtemp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            output = result.stdout.decode('utf-8')
            # Parse the output to find the temperature
            for line in output.splitlines():
                if "Temperature" in line:
                    # Example output line: "Temperature: 45 C"
                    temp = int(line.split(":")[1].strip().split(" ")[0])
                    print(f"Using AMD backup method")
                    return temp
        except:
            return None
            
    def __get_amd_gpu_usage(self):
        import subprocess
        try:
            result = subprocess.run(['/opt/rocm/bin/rocm-smi', '--showusage'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            output = result.stdout.decode('utf-8')
            # Parse the output to find the usage
            for line in output.splitlines():
                if "GPU Util" in line:
                    # Example output line: "GPU Util: 50 %"
                    usage = int(line.split(":")[1].strip().split(" ")[0])
                    print(f"Using AMD backup method")
                    return usage
        except:
            return None

    def __get_intel_gpu_temp(self):
        import subprocess
        try:
            result = subprocess.run(['intel_gpu_top', '-l', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            output = result.stdout.decode('utf-8')
            # Parse the output for temperature line
            for line in output.splitlines():
                if "temperature" in line:
                    # Example: temperature = 45 C
                    temp = int(line.split(":")[1].strip().split(" ")[0])
                    return temp
        except:
            return None

    def __get_intel_gpu_usage(self):
        import subprocess
        try:
            result = subprocess.run(['intel_gpu_top', '-b', '-l', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            output = result.stdout.decode('utf-8')
            # Parse the output for utilization
            for line in output.splitlines():
                if "Usage" in line:
                    # Example: Usage: 45%
                    usage = int(line.split(":")[1].strip().replace('%', '').strip())
                    return usage
        except:
            return None

    def get_gpu_temp(self):
        match self.gpuModel:
            case "Nvidia":
                return self.__get_nvidia_gpu_temp()
            case "AMD":
                return self.__get_amd_gpu_temp()
            case "Intel":
                return self.__get_intel_gpu_temp()
            case _:
                return None

    def get_gpu_usage(self):
        match self.gpuModel:
            case "Nvidia":
                return self.__get_nvidia_gpu_usage()
            case "AMD":
                return self.__get_amd_gpu_usage()
            case "Intel":
                return self.__get_intel_gpu_usage()
            case _:
                return None

    def get_cpu_usage(self):
        import psutil
        try:
            return int(psutil.cpu_percent(interval=1))
        except:
            return None

    def get_cpu_temp(self):
        import psutil
        try:
            temperatures = psutil.sensors_temperatures()
            if self.cpuModel == "Intel":
                temp = temperatures['coretemp'][0][1]
            elif self.cpuModel == "AMD":
                temp = temperatures['k10temp'][0][1]
            return int(temp)
        except:
            return None

class WindowsHardwareLib:
    def __init__(self):
        self.c = None
        self.initialize()
        if "Intel" in self.c.Hardware[0].get_Name():
            self.cpuModel = "Intel"
        elif "AMD" in self.c.Hardware[0].get_Name():
            self.cpuModel = "AMD"
        else:
            print("Hardware Warning: Unhandled CPU", self.c.Hardware[1].get_Name())
            self.cpuModel = None
        
        if "NVIDIA" in self.c.Hardware[1].get_Name():
            self.gpuModel = "Nvidia"
        elif "AMD" in self.c.Hardware[1].get_Name():
            self.gpuModel = "AMD"
        elif "Intel" in self.c.Hardware[1].get_Name():
            self.gpuModel = "Intel"
        else:
            print("Hardware Warning: Unhandled GPU", self.c.Hardware[1].get_Name())
            self.gpuModel = None
            
        self.driver = "Windows"
        
        print(f"Hardware Info: Platform established as {self.driver} running on {self.cpuModel} CPU with {self.gpuModel} GPU")

    def initialize(self):
        import clr  # Importing inside a method
        clr.AddReference(r'lib/OpenHardwareMonitorLib')
        from OpenHardwareMonitor import Hardware
        self.c = Hardware.Computer()
        self.c.Open()
        self.c.CPUEnabled = True
        self.c.GPUEnabled = True

    def get_cpu_temp(self):
        temp = None
        self.c.Hardware[0].Update()
        for a in range(0, len(self.c.Hardware[0].Sensors)):
            #print(self.c.Hardware[0].Sensors[a].Identifier)
            if "/temperature" in str(self.c.Hardware[0].Sensors[a].Identifier):
                temp = int(self.c.Hardware[0].Sensors[a].get_Value())
        return temp
        
    def get_gpu_temp(self):
        self.c.Hardware[1].Update()
        for a in range(0, len(self.c.Hardware[1].Sensors)):
            #print(self.c.Hardware[1].Sensors[a].Identifier)
            if "/temperature" in str(self.c.Hardware[1].Sensors[a].Identifier):
                return int(self.c.Hardware[1].Sensors[a].get_Value())
        return None

    def get_cpu_usage(self):
        load = None
        self.c.Hardware[0].Update()
        for a in range(0, len(self.c.Hardware[0].Sensors)):
            #print(self.c.Hardware[0].Sensors[a].Identifier)
            if "/load" in str(self.c.Hardware[0].Sensors[a].Identifier):
                load = int(self.c.Hardware[0].Sensors[a].get_Value())
        return load
        
    def get_gpu_usage(self):
        self.c.Hardware[1].Update()
        for a in range(0, len(self.c.Hardware[1].Sensors)):
            #print(self.c.Hardware[1].Sensors[a].Identifier)
            if "/load" in str(self.c.Hardware[1].Sensors[a].Identifier):
                return int(self.c.Hardware[1].Sensors[a].get_Value())
        return None
    
    
class DummyHarwareLib:
    def __init__(self):
        self.gpuModel = None
        self.cpuModel = None
        self.driver = "Dummy"
        print(f"Hardware Warning: {self.driver} driver")
    def get_gpu_temp(self):
        return None
    def get_gpu_usage(self):
        return None
    def get_cpu_usage(self):
        return None
    def get_cpu_temp(self):
        return None

class HardwareLib:
    def __init__(self):
        try:
            if platform.system() == 'Linux':
                self.lib = LinuxHardwareLib()
            elif platform.system() == 'Windows':
                self.lib = WindowsHardwareLib()
            else:
                self.lib = DummyHarwareLib()
        except:
            print(f"Hardware Error: {platform.system()} driver failed to Initialize")
            self.lib = DummyHarwareLib()
            
        self.gpuModel = self.lib.gpuModel
        self.cpuModel = self.lib.cpuModel
        
    def get_gpu_temp(self):
        return self.lib.get_gpu_temp()

    def get_gpu_usage(self):
        return self.lib.get_gpu_usage()

    def get_cpu_usage(self):
        return self.lib.get_cpu_usage()

    def get_cpu_temp(self):
        return self.lib.get_cpu_temp()


if __name__ == "__main__":
    probe = HardwareLib()
    print("CPU TEMP:", f'{probe.get_cpu_temp()}c')
    print("CPU USAGE:", f'{probe.get_cpu_usage()}%')
    print("GPU TEMP:", f'{probe.get_gpu_temp()}c')
    print("GPU USAGE:", f'{probe.get_gpu_usage()}%')
