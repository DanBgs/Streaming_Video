import socket
import subprocess
import tkinter as tk
from tkinter import messagebox

HOST = '0.0.0.0'  # Accetta connessioni da qualsiasi indirizzo IP
PORT = 9998


class VideoServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server di Streaming Video")

        # Variabili per gestire il processo del server e FFmpeg
        self.server_socket = None
        self.conn = None
        self.ffmpeg = None
        self.is_streaming = False

        # Label per lo stato
        self.status_label = tk.Label(root, text="Stato: Inattivo", font=("Arial", 12))
        self.status_label.pack(pady=20)

        # Pulsante per avviare la trasmissione
        self.start_button = tk.Button(root, text="Avvia Trasmissione", command=self.start_streaming, font=("Arial", 12))
        self.start_button.pack(pady=10)

        # Pulsante per fermare la trasmissione
        self.stop_button = tk.Button(root, text="Ferma Trasmissione", command=self.stop_streaming, font=("Arial", 12),
                                     state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def start_streaming(self):
        if self.is_streaming:
            messagebox.showinfo("Errore", "La trasmissione è già attiva.")
            return

        # Crea e configura il socket server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        self.status_label.config(text="Stato: In attesa di connessione...")

        print(f"[SERVER] In ascolto su {HOST}:{PORT}...")

        try:
            # Accetta una connessione in ingresso
            self.conn, addr = self.server_socket.accept()
            print(f"[SERVER] Connessione da {addr}")
            self.status_label.config(text="Stato: Connessione stabilita. Trasmettendo video...")

            # Avvia FFmpeg per trasmettere video in MPEG-TS
            self.ffmpeg = subprocess.Popen([
                'ffmpeg',
                '-re',
                '-i', 'video1.mp4',  # Sostituire con il file video desiderato
                '-f', 'mpegts',
                '-codec:v', 'mpeg1video',
                '-codec:a', 'mp2',
                '-'
            ], stdout=subprocess.PIPE)

            # Avvia un thread per inviare il flusso al client
            self.send_data_to_client()

            # Modifica i pulsanti
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.is_streaming = True
        except Exception as e:
            print(f"[SERVER] Errore: {e}")
            messagebox.showerror("Errore", f"Errore durante la connessione: {e}")

    def send_data_to_client(self):
        try:
            while True:
                data = self.ffmpeg.stdout.read(1024)
                if not data:
                    break
                self.conn.sendall(data)
        except BrokenPipeError:
            print("[SERVER] Il client ha chiuso la connessione.")
        finally:
            self.stop_streaming()

    def stop_streaming(self):
        if not self.is_streaming:
            messagebox.showinfo("Errore", "La trasmissione non è attiva.")
            return

        try:
            # Ferma la trasmissione, chiudi il socket e termina FFmpeg
            if self.conn:
                self.conn.close()
            if self.ffmpeg:
                self.ffmpeg.terminate()
            if self.server_socket:
                self.server_socket.close()

            self.status_label.config(text="Stato: Inattivo")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.is_streaming = False
            print("[SERVER] Trasmissione fermata.")
        except Exception as e:
            print(f"[SERVER] Errore durante la chiusura: {e}")
            messagebox.showerror("Errore", f"Errore durante la chiusura della trasmissione: {e}")


# Creazione della finestra principale
root = tk.Tk()
app = VideoServerApp(root)

# Avvio dell'applicazione
root.geometry("400x300")
root.mainloop()
