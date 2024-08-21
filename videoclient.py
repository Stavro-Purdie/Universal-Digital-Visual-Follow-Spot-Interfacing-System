## Intellectual property of Stavros Purdie, 2024
## This program is designed to be run on the main controller to recieve the streamed video over the network
import sys
import cv2
import socket
import struct
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal, QObject, Qt

class VideoCaptureClient(QObject):
    update_frame_signal = pyqtSignal(np.ndarray)  # Signal to update the frame in the GUI

    def __init__(self, host='localhost', port=8000, parent=None):
        super().__init__(parent)
        self.running = True  # Flag to control the client loop
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))  # Connect to the video server
        self.timer = QTimer(self)  # Timer to periodically receive frames
        self.timer.timeout.connect(self.receive_frame)
        self.timer.start(30)  # Set the timer to call receive_frame every 30 ms

    def receive_frame(self):
        try:
            # Receive the size of the frame
            message_size = self.client_socket.recv(struct.calcsize("L"))
            if not message_size:
                return
            message_size = struct.unpack("L", message_size)[0]

            # Receive the frame data
            data = b""
            while len(data) < message_size:
                packet = self.client_socket.recv(message_size - len(data))
                if not packet:
                    break
                data += packet

            # Decode the frame data to an image
            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                self.update_frame_signal.emit(frame)  # Emit the frame for updating the GUI
        except Exception as e:
            print(f"Error receiving frame: {e}")

    def stop(self):
        self.running = False  # Stop the client loop
        self.client_socket.close()  # Close the connection to the server

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Video Client")

        # Initialize the client for video capture
        self.video_client = VideoCaptureClient(host='localhost', port=8000)
        self.video_client.update_frame_signal.connect(self.update_frame)

        # Set up the main window layout
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Create a QLabel for displaying the video
        self.label = QLabel()
        self.label.setFixedSize(640, 480)  # Set fixed size for the video display
        self.main_layout.addWidget(self.label)

    def update_frame(self, frame):
        # Convert the frame to QImage for displaying in the QLabel
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Scale the pixmap while maintaining aspect ratio
        scaled_pixmap = QPixmap.fromImage(qt_img).scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)  # Update the QLabel with the scaled pixmap

    def closeEvent(self, event):
        self.video_client.stop()  # Stop the video client when closing the window
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())