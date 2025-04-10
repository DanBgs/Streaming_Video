import socket
import cv2
import pickle
import struct

def crea_client():
    host = 'localhost'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[INFO] Connesso a {host}:{port}")

    data = b""
    payload_size = struct.calcsize("!L")

    try:
        while True:
            # Ricevi la dimensione del pacchetto
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet

            if not data:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("!L", packed_msg_size)[0]

            # Ricevi il pacchetto vero e proprio (frame JPEG)
            while len(data) < msg_size:
                data += client_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            cv2.imshow("Video Streaming (TCP)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        print("[INFO] Connessione chiusa.")
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    crea_client()
