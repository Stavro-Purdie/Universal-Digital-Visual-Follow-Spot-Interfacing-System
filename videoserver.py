## Intellectual property of Stavros Purdie, 2024
## This program is designed to be run on the Nodes attached to the lights (The Raspi's) to stream video over the network
import cv2
import socket
import struct
import pickle
import threading

class VideoServer(threading.Thread):
    def __init__(self, stream_source, host='0.0.0.0', port=8000):
        super().__init__()
        self.stream_source = stream_source
        self.host = host
        self.port = port
        self.running = True

    def run(self):
        # Set up the video capture
        cap = cv2.VideoCapture(self.stream_source)
        if not cap.isOpened():
            print(f"Failed to open video stream: {self.stream_source}")
            return

        # Set up socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}...")

        # Accept a connection
        client_socket, _ = server_socket.accept()
        print("Client connected.")

        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture video frame.")
                break

            # Serialize and send the frame
            data = pickle.dumps(frame)
            message_size = struct.pack("L", len(data))
            client_socket.sendall(message_size + data)

        cap.release()
        server_socket.close()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    server = VideoServer('/dev/video0')  # Change this to your camera device
    server.start()