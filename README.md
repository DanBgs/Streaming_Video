# 🎥 Streaming Video via TCP con Python e FFmpeg

Questo progetto implementa un sistema di **streaming video tramite socket TCP** in Python. Il progetto include un **server** che invia un flusso video (da un file video locale) tramite TCP e un **client** che riceve il flusso e lo riproduce in tempo reale utilizzando **FFplay**.

### 🖥️ **Server**:

* Trasmette un file video (ad esempio, **`video1.mp4`**) in tempo reale tramite socket TCP
* Utilizza **FFmpeg** per convertire il video in un flusso **MPEG-TS** (con video e audio compressi) per ridurre la larghezza di banda

### 💻 **Client**:

* Si connette al server via TCP
* Riceve il flusso video e lo riproduce in tempo reale usando **FFplay**

## 🎞️ Funzionalità

*  Trasmissione video in tempo reale via TCP utilizzando il protocollo **MPEG-TS**
*  Trasmissione di file video locali (**MP4**) dal server al client
*  Utilizzo di **FFmpeg** per la codifica e il flusso del video
*  Riproduzione in tempo reale del flusso video tramite **FFplay** sul client
*  Compatibile con Python 3.7+

---

## 🛠️ Requisiti

1. **Python 3.7+**: Python scaricato sul proprio dispositivo

2. **FFmpeg**: FFmpeg è necessario per la codifica video e la trasmissione tramite il server, nonché per la riproduzione tramite **FFplay** sul client

   Per scaricare FFmpeg ussare il link [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html), inoltre, assicurarsi che il comando `ffmpeg` sia disponibile nel proprio PATH.


## 🚀 Come Usare il Progetto

### 1. **Avvio del Server**

Eseguire il server per iniziare a trasmettere il flusso video:

Avviato il server, esso ascolterà sulla porta **9998** (modificabile se necessario). Dopo aver avviato il server, il client può connettersi e iniziare a ricevere il flusso video.

### 2. **Avvio del Client**

Eseguire il client per ricevere e riprodurre il flusso video:

Il client si connetterà al server in ascolto su **127.0.0.1:9998** (l'IP del server è modificabile nel codice se necessario).

### 3. **Interfaccia Grafica**

Il client include un'interfaccia grafica basata su **Tkinter** che permette di avviare e fermare la ricezione del flusso video tramite pulsanti.

* **Avvia Ricezione**: Clicca per avviare la ricezione del flusso video dal server.
* **Ferma Ricezione**: Clicca per fermare la ricezione del video.

---

## ⚙️ Dettagli Tecnici

* **Server**: Il server utilizza **FFmpeg** per leggere un file video (ad esempio, `video1.mp4`), lo converte in un flusso video **MPEG-TS** e lo invia via socket TCP al client.
* **Client**: Il client riceve i dati video dal server e li invia a **FFplay** tramite pipe per la riproduzione in tempo reale.

---

## 📝 Considerazioni Finali

* Questo progetto è progettato per dimostrare la trasmissione di flussi video via TCP. Puo essere espanso ulteriormente aggiungendo funzionalità come la gestione di più client, la trasmissione di flussi video in diretta o l'inclusione di un'interfaccia utente avanzata.


