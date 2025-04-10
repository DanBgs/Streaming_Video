import socket
import cv2
import pickle
import struct
import os


def crea_server(video_path):
    if not os.path.exists(video_path):
        print(f"[ERRORE] Il file video '{video_path}' non esiste.")
        return

    host = 'localhost'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print(f"[INFO] Server in ascolto su {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"[INFO] Connessione accettata da {addr}")

    cap = cv2.VideoCapture(video_path)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[INFO] Fine del file video.")
                break

            # Comprimi il frame in JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_pickle = pickle.dumps(buffer)

            # Invia dimensione + frame
            msg = struct.pack("!L", len(frame_pickle)) + frame_pickle
            conn.sendall(msg)

            # Imposta il framerate (es. 60 fps = 17ms tra i frame)
            cv2.waitKey(17)

    finally:
        cap.release()
        conn.close()
        server_socket.close()
        print("[INFO] Server chiuso.")


if __name__ == "__main__":
    # Sostituisci con il percorso del tuo file video
    crea_server("sample-video.mp4")
