import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QTreeWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt
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

        # Setup the tree widget for selecting fixtures
        self.setup_tree_widget()

        # Track the previously selected fixture
        self.previous_selected_fixture = None

        # Connect tree widget selection change to resizing logic
        self.fixtureTreeWidget.itemSelectionChanged.connect(self.on_fixture_selected)

    def setup_tree_widget(self):
        fixtures = ["videoStream1", "videoStream2", "videoStream3"]
        for fixture in fixtures:
            item = QTreeWidgetItem([fixture])
            self.fixtureTreeWidget.addTopLevelItem(item)

    def update_frame(self, label, label_name):
        cap = self.caps[label_name]
        ret, frame = cap.read()
        if ret:
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
            prev_label.setFixedSize(320, 240)  # Shrink the previously selected camera

        # Enlarge the newly selected camera
        selected_label = self.findChild(QLabel, selected_fixture)
        selected_label.setFixedSize(640, 480)  # Enlarge the selected camera

        # Update the previously selected fixture
        self.previous_selected_fixture = selected_fixture

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
