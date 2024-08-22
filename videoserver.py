## Intellectual property of Stavros Purdie, 2024
## This program is designed to be run on the Nodes attached to the lights (The Raspi's) to stream video over the network
import cv2
import socket
import struct
import threading
from queue import Queue, Empty

class VideoServer(threading.Thread):
    def __init__(self, stream_source, host='0.0.0.0', port=8000):
        super().__init__()
        self.stream_source = stream_source  # Source of the video stream (e.g., camera device)
        self.host = host  # Host IP address for the server
        self.port = port  # Port number for the server
        self.running = True  # Flag to control the server loop
        self.client_queues = {}  # Dictionary to keep track of client-specific queues
        self.client_sockets = {}  # Dictionary to keep track of client sockets
        self.lock = threading.Lock()  # Lock for managing access to client dictionaries

    def run(self):
        print("Starting server...")
        # Open video capture from the specified source
        cap = cv2.VideoCapture(self.stream_source)
        if not cap.isOpened():
            print(f"Failed to open video stream: {self.stream_source}")
            return

        # Start a thread to produce video frames
        producer_thread = threading.Thread(target=self.produce_frames, args=(cap,))
        producer_thread.start()

        # Set up socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)  # Allow up to 5 clients to connect
        print(f"Server listening on {self.host}:{self.port}...")

        while self.running:
            try:
                # Accept new client connections
                client_socket, _ = server_socket.accept()
                print("Client connected.")

                # Create a queue for the new client
                client_queue = Queue(maxsize=10)
                with self.lock:
                    self.client_queues[client_socket] = client_queue
                    self.client_sockets[client_socket] = client_socket

                # Start a thread to handle communication with the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_queue))
                client_thread.start()

            except Exception as e:
                print(f"Server error: {e}")

        # Clean up: release video capture and close all client sockets
        cap.release()
        producer_thread.join()
        server_socket.close()
        print("Server stopped.")

    def produce_frames(self, cap):
        while self.running:
            ret, frame = cap.read()  # Capture a frame from the video source
            if not ret:
                print("Failed to capture video frame.")
                break

            # Encode the frame as JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
            if not result:
                print("Failed to encode frame.")
                continue

            data = encoded_frame.tobytes()  # Convert the encoded frame to bytes
            with self.lock:
                # Put the frame data into each client's queue
                for queue in self.client_queues.values():
                    if not queue.full():
                        queue.put(data)

        # Signal end of stream to all clients
        for queue in self.client_queues.values():
            queue.put(None)

    def handle_client(self, client_socket, client_queue):
        while self.running:
            try:
                # Retrieve frame data from the client's queue
                data = client_queue.get(timeout=1)
                if data is None:
                    break  # End of stream signal

                # Send the frame size and data to the client
                message_size = struct.pack("L", len(data))
                client_socket.sendall(message_size + data)
            except (BrokenPipeError, ConnectionResetError, Empty) as e:
                print(f"Client connection error: {e}")
                break

        # Remove client from tracking dictionaries and close the connection
        with self.lock:
            if client_socket in self.client_queues:
                del self.client_queues[client_socket]
            if client_socket in self.client_sockets:
                del self.client_sockets[client_socket]
        client_socket.close()

    def stop(self):
        self.running = False  # Stop the server loop
        with self.lock:
            # Close all client connections
            for sock in self.client_sockets.values():
                sock.close()

if __name__ == "__main__":
    server = VideoServer('/dev/video0')  # Initialize server with camera device
    server.start()