import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QTreeWidget, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QDialog
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import cv2
import numpy as np
import json
import os


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


# New class for the Camera Window
class CameraWindow(QDialog):
    def __init__(self, stream_source, parent=None):
        super(CameraWindow, self).__init__(parent)
        self.setWindowTitle("Camera Feed")
        self.setGeometry(100, 100, 640, 480)  # Set initial window size

        # Layout for the video feed
        layout = QVBoxLayout()
        self.label = QLabel()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Initialize the video stream
        self.cap = cv2.VideoCapture(stream_source)
        if not self.cap.isOpened():
            print(f"Failed to open video stream: {stream_source}")
            self.close()
            return

        # Timer for updating the video feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            height, width, _ = frame.shape
            center_x = width // 2
            center_y = height // 2
            radius = min(width, height) // 10  # Main circle radius

            # Draw the main green circle
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 3)  # Green circle

            # Calculate the inner circle radius
            inner_radius = radius // 3

            # Draw the crosshair lines outside the inner circle
            cv2.line(frame, (center_x, center_y - radius), (center_x, center_y - inner_radius), (0, 255, 0), 2)
            cv2.line(frame, (center_x, center_y + inner_radius), (center_x, center_y + radius), (0, 255, 0), 2)
            cv2.line(frame, (center_x - radius, center_y), (center_x - inner_radius, center_y), (0, 255, 0), 2)
            cv2.line(frame, (center_x + inner_radius, center_y), (center_x + radius, center_y), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), inner_radius, (0, 255, 0), 2)  # Inner green circle

            # Draw the halo around the outer circle
            halo_thickness = int(radius * 0.3)  # 30% thickness by default
            overlay = frame.copy()
            cv2.circle(overlay, (center_x, center_y), radius + halo_thickness // 2, (0, 255, 0), halo_thickness)
            alpha = 0.3  # Transparency factor for the halo
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # Convert the frame to QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            # Scale the pixmap while maintaining the aspect ratio
            scaled_pixmap = QPixmap.fromImage(qt_img).scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)


# Main Window Class
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('camui.ui', self)  # Load the UI file

        # Initialize video streams
        self.video_streams = {spot: details["URI"] for spot, details in camerapatch.items()}
        print(self.video_streams)

        # Dictionary to store OpenCV VideoCapture objects
        self.caps = {}

        # Create a timer for each video stream to update the frame
        self.timers = {}

        # Dictionary to store QLabel for each fixture
        self.labels = {}

        # Create layout for the main window
        self.main_layout = QVBoxLayout()  # Vertical layout for the main window
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Create a splitter to manage space between tree view and video labels
        self.splitter = QSplitter(Qt.Orientation.Vertical)

        # Create a layout to hold labels at the bottom
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()  # Add stretchable space to align labels to the bottom

        # Create a widget for the tree view and add it to the splitter
        self.tree_widget_container = QWidget()
        self.tree_widget_layout = QVBoxLayout(self.tree_widget_container)
        self.tree_widget_layout.addWidget(self.fixtureTreeWidget)
        self.splitter.addWidget(self.tree_widget_container)

        # Create a widget for the bottom labels layout and add it to the splitter
        self.labels_container = QWidget()
        self.labels_container.setLayout(self.bottom_layout)
        self.splitter.addWidget(self.labels_container)

        # Add the splitter to the main layout
        self.main_layout.addWidget(self.splitter)

        # Dynamically create labels and timers for each video stream
        for label_name, stream_source in self.video_streams.items():
            self.caps[label_name] = cv2.VideoCapture(stream_source)
            if not self.caps[label_name].isOpened():
                print(f"Failed to open video stream: {stream_source}")
                sys.exit(-1)

            # Create a QLabel for each video stream with a fixed initial size
            label = QLabel()
            label.setFixedSize(320, 240)  # Set initial size for the camera widget
            self.labels[label_name] = label
            self.bottom_layout.addWidget(label)  # Add label to the bottom layout

            # Create and start the timer for updating the frame
            self.timers[label_name] = QTimer(self)
            self.timers[label_name].timeout.connect(lambda l=label, n=label_name: self.update_frame(l, n))
            self.timers[label_name].start(30)  # Update every 30ms

        # Setup the tree widget for selecting fixtures
        self.setup_tree_widget()

        # Track the previously selected fixture
        self.previous_selected_fixture = None

        # Connect tree widget selection change to resizing logic
        self.fixtureTreeWidget.itemSelectionChanged.connect(self.on_fixture_selected)

        # Automatically select the first fixture on startup
        self.select_first_fixture()

    def setup_tree_widget(self):
        fixtures = list(camerapatch.keys())
        for fixture in fixtures:
            item = QTreeWidgetItem([fixture])
            self.fixtureTreeWidget.addTopLevelItem(item)

    def update_frame(self, label, label_name):
        if label is None:
            print(f"No QLabel found for '{label_name}'")
            return

        cap = self.caps.get(label_name)
        if cap is None:
            print(f"No VideoCapture found for '{label_name}'")
            return

        ret, frame = cap.read()
        if ret:
            height, width, _ = frame.shape
            center_x = width // 2
            center_y = height // 2
            radius = min(width, height) // 10  # Main circle radius

            # Draw the main green circle
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 3)  # Green circle

            # Calculate the inner circle radius
            inner_radius = radius // 3

            # Draw the crosshair lines outside the inner circle
            cv2.line(frame, (center_x, center_y - radius), (center_x, center_y - inner_radius), (0, 255, 0), 2)
            cv2.line(frame, (center_x, center_y + inner_radius), (center_x, center_y + radius), (0, 255, 0), 2)
            cv2.line(frame, (center_x - radius, center_y), (center_x - inner_radius, center_y), (0, 255, 0), 2)
            cv2.line(frame, (center_x + inner_radius, center_y), (center_x + radius, center_y), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), inner_radius, (0, 255, 0), 2)  # Inner green circle

            # Draw the halo around the outer circle
            halo_thickness = int(radius * 0.3)  # 30% thickness by default
            overlay = frame.copy()
            cv2.circle(overlay, (center_x, center_y), radius + halo_thickness // 2, (0, 255, 0), halo_thickness)
            alpha = 0.3  # Transparency factor for the halo
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # Convert the frame to QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            # Scale the pixmap while maintaining the aspect ratio
            scaled_pixmap = QPixmap.fromImage(qt_img).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

    def on_fixture_selected(self):
        selected_items = self.fixtureTreeWidget.selectedItems()
        if selected_items:
            selected_fixture = selected_items[0].text(0)

            # Open a new window for the selected camera
            self.open_camera_window(selected_fixture)

    def open_camera_window(self, selected_fixture):
        stream_source = self.video_streams.get(selected_fixture)
        if stream_source:
            camera_window = CameraWindow(stream_source, self)
            camera_window.exec()  # Show the camera window as a modal dialog

    def select_first_fixture(self):
        if self.fixtureTreeWidget.topLevelItemCount() > 0:
            self.fixtureTreeWidget.topLevelItem(0).setSelected(True)
            self.on_fixture_selected()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())