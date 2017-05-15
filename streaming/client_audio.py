# CODE CLIENT AUDIO
# coding=utf-8

import socket
import pyaudio

s = socket.socket()
host = socket.gethostname()
port = 60000
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Démarrage de la connexion avec le serveur
s.connect((host, port))
s.send("GET /beta.wav HTTP/1.0")

# Paramétrage de l'audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# Débuter l'enregistrement et la lecture
with open('record.wav', 'wb') as f:
    while True:
        print('receiving data...')
        data = s.recv(CHUNK)
        print('data=%s', (data))
        if not data:
            break
        # Ecriture dans le fichier de sauvegarde
        f.write(data)
        # Lecture audio du stream
        stream.write(data)

# Fermeture canaux
f.close()
stream.stop_stream()
stream.close()
p.terminate()
s.close()
print('File recorded - connection closed')
