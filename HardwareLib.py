import psutil
import subprocess
import json
import platform

class HardwareLib:

    def __init__(self):
        if self.get_nvidia_gpu_temp():
            self.gpuModel = "Nvidia"
        elif self.get_amd_gpu_temp():
            self.gpuModel = "AMD"
        elif self.get_intel_gpu_temp():
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
        print(f"Hardware Info: Platform established as Linux running on {self.cpuModel} CPU with {self.gpuModel} GPU")

    def get_nvidia_gpu_temp(self):
        try:
            result = subprocess.run(['/usr/bin/nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            temp = result.stdout.decode('utf-8').strip()
            return int(temp)
        except:
            return None

    def get_nvidia_gpu_usage(self):
        try:
            result = subprocess.run(['/usr/bin/nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            usage = result.stdout.decode('utf-8').strip()
            return int(usage)
        except:
            return None

    def get_amd_gpu_temp(self):
        try:
            temperatures = psutil.sensors_temperatures()
            return int(temperatures['amdgpu'][0][1])
        except:
            return get_amd_gpu_temp_backup()

    def get_amd_gpu_temp_backup(self):
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
            
    def get_amd_gpu_usage(self):
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

    def get_intel_gpu_temp(self):
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

    def get_intel_gpu_usage(self):
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
                return self.get_nvidia_gpu_temp()
            case "AMD":
                return self.get_amd_gpu_temp()
            case "Intel":
                return self.get_intel_gpu_temp()
            case _:
                return None

    def get_gpu_usage(self):
        match self.gpuModel:
            case "Nvidia":
                return self.get_nvidia_gpu_usage()
            case "AMD":
                return self.get_amd_gpu_usage()
            case "Intel":
                return self.get_intel_gpu_usage()
            case _:
                return None

    def get_cpu_usage(self):
        try:
            return int(psutil.cpu_percent(interval=1))
        except:
            return None

    def get_cpu_temp(self):
        try:
            temperatures = psutil.sensors_temperatures()
            if self.cpuModel == "Intel":
                temp = temperatures['coretemp'][0][1]
            elif self.cpuModel == "AMD":
                temp = temperatures['k10temp'][0][1]
            return int(temp)
        except:
            return None
