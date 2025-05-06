import socket
import subprocess

SERVER_IP = '127.0.0.1'
PORT = 9999

# Crea socket e si connette al server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"[CLIENT] Connesso a {SERVER_IP}:{PORT}")

# Avvia FFplay per riprodurre lo stream MPEG-TS ricevuto
ffplay = subprocess.Popen([
    'ffplay', '-i', 'pipe:0', '-fflags', 'nobuffer'
], stdin=subprocess.PIPE)

# Legge dal socket e scrive nel player
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    ffplay.stdin.write(data)

client_socket.close()
ffplay.terminate()
print("[CLIENT] Streaming terminato.")
