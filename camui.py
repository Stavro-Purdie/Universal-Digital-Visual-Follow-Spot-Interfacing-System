import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QTreeWidget, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QDialog
from PyQt6.QtGui import QPixmap, QImage, QMouseEvent, QPainter, QColor
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QPoint
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

class DraggableLabel(QLabel):
    position_changed = pyqtSignal(QPoint)
    
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.offset = QPoint(0, 0)
        self.center = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos() - self.center

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.center = event.pos() - self.offset
            self.position_changed.emit(self.center)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def draw_aiming_system(self, frame):
        h, w = frame.shape[:2]
        if self.center is None:
            self.center = QPoint(w // 2, h // 2)

        center_x, center_y = self.center.x(), self.center.y()

        cv2.circle(frame, (center_x, center_y), 40, (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 15, (0, 255, 0), 2)
        cv2.line(frame, (center_x - 40, center_y), (center_x - 15, center_y), (0, 255, 0), 2)
        cv2.line(frame, (center_x + 15, center_y), (center_x + 40, center_y), (0, 255, 0), 2)
        cv2.line(frame, (center_x, center_y - 40), (center_x, center_y - 15), (0, 255, 0), 2)
        cv2.line(frame, (center_x, center_y + 15), (center_x, center_y + 40), (0, 255, 0), 2)

        return frame

class VideoCaptureThread(QThread):
    update_frame_signal = pyqtSignal(np.ndarray)

    def __init__(self, uri, label):
        super().__init__()
        self.uri = uri
        self.label = label
        self.cap = cv2.VideoCapture(uri)
        if not self.cap.isOpened():
            print(f"Failed to open video stream: {uri}")
            self.cap.release()

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = self.label.draw_aiming_system(frame)
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

def sync_position(position, labels):
    for label in labels:
        label.center = position
        label.update()

def on_fixture_selected(tree_widget, video_streams, main_label, main_thread):
    selected_items = tree_widget.selectedItems()
    if selected_items:
        selected_fixture = selected_items[0].text(0)
        print(f"Selected fixture: {selected_fixture}")

        if main_thread is not None:
            main_thread.stop()

        main_thread = VideoCaptureThread(video_streams[selected_fixture], main_label)
        main_thread.update_frame_signal.connect(lambda frame, l=main_label: update_frame(l, frame))
        main_label.position_changed.connect(lambda pos, s=selected_fixture: sync_position(pos, [label for label in small_views.values() if label.stream_id == s]))
        main_thread.start()

def select_first_fixture(tree_widget):
    if tree_widget.topLevelItemCount() > 0:
        tree_widget.topLevelItem(0).setSelected(True)

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    ## Take URI, if URI has no prefix, add one, If it does, Leave it
    video_streams = {
        spot: f"http://{details['URI']}" if not details["URI"].startswith(("http://", "https://", "rtsp://")) else details["URI"]
        for spot, details in camerapatch.items()
    }

    main_thread = None

    main_layout = QVBoxLayout()
    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    window.setCentralWidget(central_widget)

    tree_widget = QTreeWidget()
    for fixture in video_streams.keys():
        item = QTreeWidgetItem([fixture])
        tree_widget.addTopLevelItem(item)
    tree_widget.itemSelectionChanged.connect(lambda: on_fixture_selected(tree_widget, video_streams, main_label, main_thread))

    main_layout.addWidget(tree_widget)

    # Main camera view
    main_label = DraggableLabel()
    main_label.setFixedSize(640, 480)
    main_layout.addWidget(main_label)

    # Multi-view window
    multiview_window = QDialog()
    multiview_window.setWindowTitle("Multi-view")
    multiview_layout = QVBoxLayout()
    multiview_window.setLayout(multiview_layout)

    # Create small views for all cameras
    global small_views
    small_views = {}
    for fixture, uri in video_streams.items():
        small_label = DraggableLabel()
        small_label.setFixedSize(160, 120)
        small_label.stream_id = fixture
        small_views[fixture] = small_label
        thread = VideoCaptureThread(uri, small_label)
        thread.update_frame_signal.connect(lambda frame, l=small_label: update_frame(l, frame))
        thread.start()
        multiview_layout.addWidget(small_label)

    multiview_window.show()
    window.show()
    QTimer.singleShot(0, lambda: select_first_fixture(tree_widget))

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
