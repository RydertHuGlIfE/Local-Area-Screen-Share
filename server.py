import socket
import struct
import cv2
import numpy as np

def receive_screenshot(conn):
    try:
        data = b""
        payload_size = struct.calcsize("Q")  # Size of the packed frame size (8 bytes)

        while True:
            # Receive the size of the incoming frame data
            while len(data) < payload_size:
                packet = conn.recv(4 * 1024)  # Buffer size
                if not packet:
                    return
                data += packet

            # Extract the message size
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            # Receive the actual frame data based on the message size
            while len(data) < msg_size:
                data += conn.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Decode the image from the received binary data using OpenCV
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Display the image using OpenCV
            if frame is not None:
                cv2.imshow("Screen Share", frame)
                cv2.waitKey(1)
            else:
                print("Failed to decode frame.")
    except Exception as e:
        print("Error receiving screenshot:", e)
    finally:
        conn.close()

def server_program():
    host = '192.168.1.60'  # Your server's IP
    port = 12345  # Port number

    try:
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(2)
        print(f"Server listening for connections on {host}:{port}")

        conn, address = server_socket.accept()
        print("Connection from:", address)

        receive_screenshot(conn)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        server_socket.close()

if __name__ == '__main__':
    server_program()
