import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QTreeWidget, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QDialog
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
import cv2
import numpy as np
import json
import os

# Load JSON Files
def load_json_files():
    os.chdir('Config/')
    def load_file(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    try:
        adatvalues = load_file('adapterconfig.json')
        fixtureprofiles = load_file('profiles.json')
        fixturepatch = load_file('patchdata.json')
        fixturealias = load_file('fixtureconfig.json')
        camerapatch = load_file('camerapatch.json')
        print('All configuration files loaded successfully.')
    except Exception as e:
        print(f"Error loading configuration files: {e}")
        sys.exit(-1)
    os.chdir('../')
    return adatvalues, fixtureprofiles, fixturepatch, fixturealias, camerapatch

adatvalues, fixtureprofiles, fixturepatch, fixturealias, camerapatch = load_json_files()


# Video capture thread class
class VideoCaptureThread(QThread):
    update_frame_signal = pyqtSignal(np.ndarray)

    def __init__(self, uri):
        super().__init__()
        self.uri = uri
        self.cap = cv2.VideoCapture(uri)
        if not self.cap.isOpened():
            print(f"Failed to open video stream: {uri}")
            self.cap.release()

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.update_frame_signal.emit(frame)
            else:
                break

    def stop(self):
        self.cap.release()
        self.quit()
        self.wait()

def update_frame(label, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = frame.shape
    bytes_per_line = ch * w
    qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    scaled_pixmap = QPixmap.fromImage(qt_img).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    label.setPixmap(scaled_pixmap)

def on_fixture_selected(tree_widget, video_streams):
    selected_items = tree_widget.selectedItems()
    if selected_items:
        selected_fixture = selected_items[0].text(0)
        print(f"Selected fixture: {selected_fixture}")

def select_first_fixture(tree_widget):
    if tree_widget.topLevelItemCount() > 0:
        tree_widget.topLevelItem(0).setSelected(True)
        on_fixture_selected(tree_widget, {})

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    # Initialize video streams with fixed URIs
    video_streams = {
        spot: f"http://{details['URI']}" if not details["URI"].startswith(("http://", "https://", "rtsp://")) else details["URI"]
        for spot, details in camerapatch.items()
    }
    labels = {}
    threads = {}

    # Create layout for the main window
    main_layout = QVBoxLayout()
    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    window.setCentralWidget(central_widget)

    # Create a splitter to manage space between tree view and video labels
    splitter = QSplitter(Qt.Orientation.Vertical)

    # Create a layout to hold labels at the bottom
    bottom_layout = QHBoxLayout()
    bottom_layout.addStretch()

    # Tree widget setup
    tree_widget = QTreeWidget()
    for fixture in video_streams.keys():
        item = QTreeWidgetItem([fixture])
        tree_widget.addTopLevelItem(item)
    tree_widget.itemSelectionChanged.connect(lambda: on_fixture_selected(tree_widget, video_streams))

    # Add tree widget and labels to the splitter
    splitter.addWidget(tree_widget)
    labels_container = QWidget()
    labels_container.setLayout(bottom_layout)
    splitter.addWidget(labels_container)

    # Add the splitter to the main layout
    main_layout.addWidget(splitter)

    # Create and start video capture threads for each video stream
    for label_name, stream_source in video_streams.items():
        label = QLabel()
        label.setFixedSize(320, 240)
        labels[label_name] = label
        bottom_layout.addWidget(label)
        
        # Create and start the video capture thread
        thread = VideoCaptureThread(stream_source)
        thread.update_frame_signal.connect(lambda frame, l=label: update_frame(l, frame))
        thread.start()
        threads[label_name] = thread

    window.show()
    QTimer.singleShot(0, lambda: select_first_fixture(tree_widget))

    sys.exit(app.exec())

# Load JSON and other variables here (from your initial code)

if __name__ == "__main__":
    main()