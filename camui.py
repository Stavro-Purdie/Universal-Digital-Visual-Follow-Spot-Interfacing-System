from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSplitter, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QObject
import sys
import os
import json
import cv2
import numpy as np
import struct
import socket
from urllib.parse import urlparse

# Import JSON Files
# Load adapter values
os.chdir('Config/')
try:
    print("Opening 'adapterconfig.json'....")
    with open('adapterconfig.json', 'r') as file:
        adatvalues = json.load(file)
    print('Adapter Config file found and loaded')
except:
    print("No Adapter Config file found, Program Quitting, Please run config.py")
    sys.exit(-1)

# Load previous fixture profiles (if there are any)
try:
    print("Opening 'profiles.json'....")
    with open('profiles.json', 'r') as file:
        fixtureprofiles = json.load(file)
    print("Fixture profile database found and loaded")
except:
    print("No Fixture Profile Database found, Program Quitting, Please run config.py")
    sys.exit(-1)

# Load previous patch (if exists)
try:
    print("Opening 'patchdata.json'....")
    with open('patchdata.json', 'r') as file:
        fixturepatch = json.load(file)
    print("Patch data found and loaded")
except:
    print("No Patch Database found, Program Quitting, Please run config.py")
    sys.exit(-1)

# Import fixture alias
try:
    print("Opening 'fixtureconfig.json'....")
    with open('fixtureconfig.json', 'r') as file:
        fixturealias = json.load(file)
    print('Fixture Alias dictionary found and loaded')
except:
    print('No Fixture Alias database found, Program Quitting, Please run config.py')
    sys.exit(-1)

# Import Camera patch
try:
    print("Opening 'camerapatch.json'....")
    with open('camerapatch.json', 'r') as file:
        camerapatch = json.load(file)
    print('Camera Patch dictionary found and loaded')
except:
    print('No Camera Patch database found, Program Quitting, Please run config.py')
os.chdir('../')  # Return to main directory

# Central Video Capture Thread
class VideoCaptureClient(QObject):
    update_frame_signal = pyqtSignal(np.ndarray, str)

    def __init__(self, uri, label_name, parent=None):
        super().__init__(parent)
        self.uri = uri
        self.label_name = label_name
        self._parse_uri()
        print(f"Connecting to {self.host}:{self.port}")
        self.running = True
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.host is None or self.port is None:
            raise ValueError("Host or port is None. Check URI parsing.")
        self.client_socket.connect((self.host, self.port))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_frame)
        self.timer.start(30)

    def _parse_uri(self):
        parsed_url = urlparse(self.uri)
        self.host = parsed_url.hostname
        self.port = parsed_url.port or 8000  # Default port if not specified
        print(f"Parsed URI: Host={self.host}, Port={self.port}")

    def receive_frame(self):
        try:
            message_size = self.client_socket.recv(struct.calcsize("L"))
            if not message_size:
                return
            message_size = struct.unpack("L", message_size)[0]
            data = b""
            while len(data) < message_size:
                packet = self.client_socket.recv(message_size - len(data))
                if not packet:
                    break
                data += packet
            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                self.update_frame_signal.emit(frame, self.label_name)
        except Exception as e:
            print(f"Error receiving frame: {e}")

    def stop(self):
        self.running = False
        self.client_socket.close()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Video Client")

        self.video_clients = {}
        self.labels = {}

        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()

        self.labels_container = QWidget()
        self.labels_container.setLayout(self.bottom_layout)
        self.splitter.addWidget(self.labels_container)
        self.main_layout.addWidget(self.splitter)

        # Create video client for each video stream
        for label_name, camera_info in camerapatch.items():
            uri = camera_info["URI"]
            label = QLabel()
            label.setFixedSize(320, 240)
            self.labels[label_name] = label
            self.bottom_layout.addWidget(label)

            client = VideoCaptureClient(uri=uri, label_name=label_name)
            client.update_frame_signal.connect(self.update_frame)
            self.video_clients[label_name] = client

    def update_frame(self, frame, label_name):
        if label_name not in self.labels:
            print(f"No QLabel found for '{label_name}'")
            return

        label = self.labels[label_name]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        scaled_pixmap = QPixmap.fromImage(qt_img).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        for client in self.video_clients.values():
            client.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())