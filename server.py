import socket
import subprocess

HOST = '0.0.0.0'
PORT = 9998

# Avvia socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[SERVER] In ascolto su {HOST}:{PORT}...")
conn, addr = server_socket.accept()
print(f"[SERVER] Connessione da {addr}")

# Avvia FFmpeg per trasmettere video.mkv in MPEG-TS
ffmpeg = subprocess.Popen([
    'ffmpeg',
    '-re',                 # Real-time streaming
    '-i', 'video.mp4',     # Input file
    '-f', 'mpegts',        # Formato streaming compatibile
    '-codec:v', 'mpeg1video',
    '-codec:a', 'mp2',
    '-'                    # Output su stdout
], stdout=subprocess.PIPE)

# Invia il flusso via socket
while True:
    data = ffmpeg.stdout.read(1024)
    if not data:
        break
    conn.sendall(data)

conn.close()
server_socket.close()
print("[SERVER] Streaming completato.")
