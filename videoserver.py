## Intellectual property of Stavros Purdie, 2024
## This program is designed to be run on the Nodes attached to the lights (The Raspi's) to stream video over the network
import cv2
import socket
import struct
import pickle
import threading
from queue import Queue

class VideoServer(threading.Thread):
    def __init__(self, stream_source, host='0.0.0.0', port=8000):
        super().__init__()
        self.stream_source = stream_source
        self.host = host
        self.port = port
        self.running = True
        self.client_sockets = []
        self.video_queue = Queue(maxsize=10)  # Queue to store frames for clients

    def run(self):
        # Set up the video capture
        cap = cv2.VideoCapture(self.stream_source)
        if not cap.isOpened():
            print(f"Failed to open video stream: {self.stream_source}")
            return

        # Start the video frame producer thread
        producer_thread = threading.Thread(target=self.produce_frames, args=(cap,))
        producer_thread.start()

        # Set up socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}...")

        while self.running:
            try:
                # Accept a new connection
                client_socket, _ = server_socket.accept()
                print("Client connected.")
                
                # Add the new client socket to the list
                self.client_sockets.append(client_socket)
                
                # Start a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
                
            except Exception as e:
                print(f"Server error: {e}")

        # Clean up
        cap.release()
        producer_thread.join()  # Ensure the producer thread has finished
        for sock in self.client_sockets:
            sock.close()
        server_socket.close()

    def produce_frames(self, cap):
        """ Produce video frames and put them in the queue """
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture video frame.")
                break
            
            # Serialize and put the frame in the queue
            data = pickle.dumps(frame)
            self.video_queue.put(data)
            
        # Signal end of stream by putting None in the queue
        self.video_queue.put(None)

    def handle_client(self, client_socket):
        """ Handle communication with a single client """
        while self.running:
            # Get frame from queue
            data = self.video_queue.get()
            if data is None:
                break  # End of stream signal
            
            # Send the frame to the client
            message_size = struct.pack("L", len(data))
            
            try:
                client_socket.sendall(message_size + data)
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Client connection error: {e}")
                client_socket.close()
                break

        # Remove client socket from the list and close it
        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
            client_socket.close()

    def stop(self):
        self.running = False
        # Stop the producer thread by closing the queue
        self.video_queue.put(None)
        for sock in self.client_sockets:
            sock.close()

## Main Routine
if __name__ == "__main__":
    server = VideoServer('/dev/video0')  # Change this to your camera device
    server.start()