import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QTreeWidget, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import cv2
import numpy as np
import json
import os

## Import JSON Files
## Load adapter values
os.chdir('Config/')
try:
    print("Opening 'adapterconfig.json'....")
    with open('adapterconfig.json', 'r') as file:
        adatvalues = json.load(file)
    print('Adapter Config file found and loaded')
except:
    print("No Adapter Config file found, Program Quitting, Please run config.py")
    sys.exit(-1)

## Load previous fixture profiles (if there are any)
try:
    print("Opening 'profiles.json'....")
    with open('profiles.json', 'r') as file:         
        fixtureprofiles = json.load(file)
    print("Fixture profile database found and loaded")
except:
    print("No Fixture Profile Database found, Program Quitting, Please run config.py")
    sys.exit(-1)

## Load previous patch (if exists)
try:
    print("Opening 'patchdata.json'....")
    with open('patchdata.json', 'r') as file:
        fixturepatch = json.load(file)
    print("Patch data found and loaded")
except:
    print("No Patch Database found, Program Quitting, Please run config.py")
    sys.exit(-1)

## Import fixture alias
try:
    print("Opening 'fixtureconfig.json'....")
    with open('fixtureconfig.json', 'r') as file:
        fixturealias = json.load(file)
    print('Fixture Alias dictionary found and loaded')
except:
    print('No Fixture Alias database found, Program Quitting, Please run config.py')
    sys.exit(-1)

## Import Camera patch
try:
    print("Opening 'camerapatch.json'....")
    with open('camerapatch.json', 'r') as file:
        camerapatch = json.load(file)
    print('Camera Patch dictionary found and loaded')
except:
    print('No Camera Patch database found, Program Quitting, Please run config.py')
os.chdir('../')     ## Return to main directory

## Business side of the program
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('camui.ui', self)  # Load the UI file

        # Initialize video streams
        self.video_streams = {spot: details["URI"] for spot, details in camerapatch.items()}
        print(self.video_streams)

        # Dictionary to store OpenCV VideoCapture objects
        self.caps = {}

        # Initialize VideoCapture for each stream
        for label_name, stream_source in self.video_streams.items():
            self.caps[label_name] = cv2.VideoCapture(stream_source)
            if not self.caps[label_name].isOpened():
                print(f"Failed to open video stream: {stream_source}")
                sys.exit(-1)

        # Create a timer for each video stream to update the frame
        self.timers = {}
        for label_name in self.video_streams.keys():
            label = self.findChild(QLabel, label_name)
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

        # Percentage control for the halo's thickness
        self.halo_percentage = 0.3  # 30% thickness by default

        # Create labels for video streams dynamically
        self.create_video_stream_labels()

    def create_video_stream_labels(self):
        layout = self.findChild(QHBoxLayout, 'horizontalLayout')  # Adjust this if needed

        for spot_name, uri in self.video_streams.items():
            # Create QLabel dynamically
            label = QLabel(self)
            label.setObjectName(spot_name)  # Set the object name for future reference
            label.setStyleSheet("background-color: black; color: white;")
            label.setText(f'{spot_name}: {uri}')
            
            # Add QLabel to the layout
            layout.addWidget(label)

    def setup_tree_widget(self):
        fixtures = list(camerapatch.keys())
        for fixture in fixtures:
            item = QTreeWidgetItem([fixture])
            self.fixtureTreeWidget.addTopLevelItem(item)

    def update_frame(self, label, label_name):
        cap = self.caps[label_name]
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
            # Vertical line
            cv2.line(frame, (center_x, center_y - radius), (center_x, center_y - inner_radius), (0, 255, 0), 2)
            cv2.line(frame, (center_x, center_y + inner_radius), (center_x, center_y + radius), (0, 255, 0), 2)
            # Horizontal line
            cv2.line(frame, (center_x - radius, center_y), (center_x - inner_radius, center_y), (0, 255, 0), 2)
            cv2.line(frame, (center_x + inner_radius, center_y), (center_x + radius, center_y), (0, 255, 0), 2)

            # Draw the smaller inner circle
            cv2.circle(frame, (center_x, center_y), inner_radius, (0, 255, 0), 2)  # Inner green circle

            # Draw the halo around the outer circle
            halo_thickness = int(radius * self.halo_percentage)  # Thickness based on percentage
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

            # Resize the newly selected camera widget
            self.resize_camera_widgets(selected_fixture)

    def resize_camera_widgets(self, selected_fixture):
        # If there was a previous selection, revert its size back
        if self.previous_selected_fixture:
            prev_label = self.findChild(QLabel, self.previous_selected_fixture)
            if prev_label:
                prev_label.setFixedSize(320, 240)  # Shrink the previously selected camera

        # Enlarge the newly selected camera
        selected_label = self.findChild(QLabel, selected_fixture)
        if selected_label:
            selected_label.setFixedSize(640, 480)  # Enlarge the selected camera

        # Update the previously selected fixture
        self.previous_selected_fixture = selected_fixture

    def select_first_fixture(self):
        # Select the first fixture in the tree widget by default
        first_item = self.fixtureTreeWidget.topLevelItem(0)
        if first_item:
            self.fixtureTreeWidget.setCurrentItem(first_item)
            self.resize_camera_widgets(first_item.text(0))

    def closeEvent(self, event):
        # Release all VideoCapture objects when the application is closed
        for cap in self.caps.values():
            cap.release()
        event.accept()

## Main Routine
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())