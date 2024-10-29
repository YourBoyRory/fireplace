import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie, QIcon 
from PyQt5.QtCore import Qt

class GifWindow(QMainWindow):

    def __init__(self, gif_path):
        super().__init__()

        self.label = QLabel(self)
        self.movie = QMovie(gif_path)
        
        self.setWindowIcon(QIcon(self.getAssetPath('icon-small.png')))

        if "--fullscreen" in sys.argv:
            self.setWindowState(Qt.WindowFullScreen)

        self.setCentralWidget(self.label)
        self.label.setMovie(self.movie)
        self.movie.start()
        self.label.setMinimumSize(800, 600)
        self.label.setScaledContents(True)

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

