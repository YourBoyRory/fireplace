import sys
import os
import random
import platform
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import Qt, QTimer
import threading
import time

class LinuxTempProber:
    
    def __init__(self, interval):
        
        from HardwareLib import LinuxHardwareLib
        
        self.status = 0
        
        self.cpuTemp = None
        self.cpuUse = None
        self.gpuTemp = None
        self.gpuUse = None
        
        self.interval = interval
        
        self.probe = LinuxHardwareLib()
        self.running = True
        self.probeThread = threading.Thread(target=self.probeTemperatures)
        self.probeThread.daemon = True  # Exit when main program exits
        self.probeThread.start()

    def probeTemperatures(self):
        while self.running:
            self.cpuTemp = self.probe.get_cpu_temp()
            self.cpuUse = self.probe.get_cpu_usage()
            self.gpuTemp = self.probe.get_gpu_temp()
            self.gpuUse = self.probe.get_gpu_usage()
            if self.cpuTemp == None or self.cpuUse == None or self.gpuTemp == None or self.gpuUse == None:
                self.running = False
                self.status = -1
            else:
                self.status = 1
            time.sleep(self.interval/1000)

    def stop(self):
        self.running = False
        self.probeThread.join()
        
class DummyTempProber:
    def __init__(self):
        self.status = -1
        self.cpuTemp = None
        self.cpuUse = None
        self.gpuTemp = None
        self.gpuUse = None
        
    def stop(self):
        pass

class GifWindow(QMainWindow):
    def __init__(self, gif_path):
        super().__init__()

        self.gif = QLabel(self)
        self.movie = QMovie(gif_path)
        if platform.system() == 'Linux':
            self.prober = LinuxTempProber(1000)
        elif platform.system() == 'Windows':
            self.prober = DummyTempProber()
        else:
            self.prober = DummyTempProber()
        
        self.setWindowIcon(QIcon(self.getAssetPath('icon-small.png')))

        if "--fullscreen" in sys.argv:
            self.setWindowState(Qt.WindowFullScreen)

        self.setCentralWidget(self.gif)
        self.gif.setMovie(self.movie)
        self.gif.setMinimumSize(800, 600)
        self.gif.setScaledContents(True)
        self.movie.start()
        
        self.tempLabel = QLabel('\n', self.gif)
        self.tempLabel.setStyleSheet("color: gray;")
        self.tempLabel.setMinimumSize(800, 0)
        self.tempLabel.move(10, 10)
        
        self.probeTempTimer = QTimer(self)
        self.probeTempTimer.timeout.connect(self.readTemperatures)
        self.probeTempTimer.start(1500)

    def readTemperatures(self):
        if self.prober.status == 1:
            info = f'CPU: {self.prober.cpuTemp}c {self.prober.cpuUse}%\nGPU: {self.prober.gpuTemp}c {self.prober.gpuUse}%'
            #print(f"Window Info:\n   {info}")
            self.tempLabel.setText(info)
        elif self.prober.status == 0: 
            pass
        else:
            print("Window Warning: Platform Not supported")
            self.tempLabel.setText(' ')
            self.prober.stop()
            self.probeTempTimer.stop()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.setWindowState(Qt.WindowNoState)
            else:
                self.setWindowState(Qt.WindowFullScreen)

    def getAssetPath(self, file):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, 'assets', file)


class GifPlayer:
    def __init__(self, gif_path):
        app = QApplication(sys.argv)
        ui = GifWindow(gif_path)
        ui.show()
        app.exec_()
