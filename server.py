import socket
import subprocess

HOST = '0.0.0.0'
PORT = 9998

# Crea e configura il socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[SERVER] In ascolto su {HOST}:{PORT}...")

# Accetta una connessione in ingresso
conn, addr = server_socket.accept()
print(f"[SERVER] Connessione da {addr}")

# Avvia FFmpeg per trasmettere video in MPEG-TS
ffmpeg = subprocess.Popen([
    'ffmpeg',
    '-re',
    '-i', 'video1.mp4',
    '-f', 'mpegts',
    '-codec:v', 'mpeg1video',
    '-codec:a', 'mp2',
    '-'
], stdout=subprocess.PIPE)

# Invia il flusso al client
try:
    while True:
        data = ffmpeg.stdout.read(1024)
        if not data:
            break
        conn.sendall(data)
except BrokenPipeError:
    print("[SERVER] Il client ha chiuso la connessione.")
finally:
    conn.close()
    server_socket.close()
    ffmpeg.terminate()
    print("[SERVER] Streaming terminato.")
