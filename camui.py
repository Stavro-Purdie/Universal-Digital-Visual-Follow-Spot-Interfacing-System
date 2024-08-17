import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer
from PyQt6 import uic
import cv2

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('camui.ui', self)  # Load the UI file

        # Initialize video streams (replace with actual stream URLs if needed)
        self.video_streams = {
            "videoStream1": 0,  # Using default webcam for testing
            "videoStream2": 0,  # Can be replaced with another video source
            "videoStream3": 0   # Can be replaced with another video source
        }

        # Dictionary to store OpenCV VideoCapture objects
        self.caps = {}

        # Initialize VideoCapture for each stream
        for label_name, stream_source in self.video_streams.items():
            self.caps[label_name] = cv2.VideoCapture(stream_source)

        # Create a timer for each video stream to update the frame
        self.timers = {}
        for label_name in self.video_streams.keys():
            label = self.findChild(QLabel, label_name)
            self.timers[label_name] = QTimer(self)
            self.timers[label_name].timeout.connect(lambda l=label, n=label_name: self.update_frame(l, n))
            self.timers[label_name].start(30)  # Update every 30ms

    def update_frame(self, label, label_name):
        cap = self.caps[label_name]
        ret, frame = cap.read()
        if ret:
            # Convert the frame to QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(qt_img))

    def closeEvent(self, event):
        # Release all VideoCapture objects when the application is closed
        for cap in self.caps.values():
            cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())