import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class FullscreenGifWindow(QMainWindow):
    
    def __init__(self, gif_path):
        super().__init__()
        self.setWindowState(Qt.WindowFullScreen)
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.movie = QMovie(gif_path)
        self.label.setMovie(self.movie)
        self.movie.start()
        self.label.setScaledContents(True)
        self.label.setGeometry(self.rect())
        self.label.setAlignment(Qt.AlignCenter)
        
    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class GifPlayer:
    def __init__(self, gif_path):
        app = QApplication(sys.argv)
        ui = FullscreenGifWindow(gif_path)
        ui.show()
        sys.exit(app.exec_())
