import sys
import os
from HardwareLib import HardwareLib
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie, QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer
import threading
import time

class TempProber:
    
    def __init__(self, interval):
        self.status = 0
        self.cpuTemp = None
        self.cpuUse = None
        self.gpuTemp = None
        self.gpuUse = None
        self.interval = interval
        self.probe = HardwareLib()
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

class GifWindow(QMainWindow):
    def __init__(self, gif_path):
        super().__init__()

        self.gif = QLabel(self)
        self.movie = QMovie(gif_path)
        self.prober = TempProber(1000)
        
        self.setWindowIcon(QIcon(self.getAssetPath('icon-small.png')))
        font_id = QFontDatabase.addApplicationFont(self.getAssetPath('font.ttf'))
        if font_id != -1:
            # Get the family name of the loaded font
            self.monoFont = QFontDatabase.applicationFontFamilies(font_id)[0]

        if "--fullscreen" in sys.argv:
            self.setWindowState(Qt.WindowFullScreen)

        self.setCentralWidget(self.gif)
        self.gif.setMovie(self.movie)
        self.gif.setMinimumSize(800, 600)
        self.gif.setScaledContents(True)
        self.movie.start()
        
        self.tempLabel = QLabel('\n', self.gif)
        self.tempLabel.setStyleSheet("color: gray;")
        self.resizeEvent = self.onResize
        
        self.probeTempTimer = QTimer(self)
        self.probeTempTimer.timeout.connect(self.readTemperatures)
        self.probeTempTimer.start(1500)

    def onResize(self, event):
        self.setLableSize()
        super().resizeEvent(event)
        
    def setLableSize(self):
        #Text
        fs = int(24 * ((self.size().width()+self.size().height())/2666))
        self.tempLabel.setFont(QFont(self.monoFont, fs)) 
        
        #Size
        self.tempLabel.adjustSize()
        x = int((self.size().width()-self.tempLabel.width())/2)
        y = int(self.size().height()-self.tempLabel.height()) - 10
        self.tempLabel.move(x, y)
        self.tempLabel.adjustSize()
        
    def readTemperatures(self):
        if self.prober.status == 1:
            cpuLable = "CPU"
            gpuLable = "GPU"
            cpuTemp = f"{self.prober.cpuTemp}c"
            cpuUse = f"{self.prober.cpuUse}%"
            gpuTemp = f"{self.prober.gpuTemp}c"
            gpuUse = f"{self.prober.gpuUse}%"
            info = f'{cpuLable:>9} ║ {gpuLable} \n{cpuTemp:>4} {cpuUse:>4} ║ {gpuUse:<4} {gpuTemp:<4}'
            #print(f"Window Info:   {info}")
            self.tempLabel.setText(info)
            self.setLableSize()
        elif self.prober.status == 0: 
            pass
        else:
            print("Window Warning: Temperature reading on this platform not supported")
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

if __name__ == "__main__":
    GifPlayer('./assets/fire.gif')
