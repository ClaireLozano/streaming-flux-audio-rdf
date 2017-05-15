# coding=utf-8

import socket, sys

import pyaudio

PORT = 7800
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

if (len(sys.argv) < 2):
    print("Not enough arguments! \n *** Usage: {0} <hostname> ***\n".format(sys.argv[0]))
    sys.exit()

HOST = sys.argv[1]

# 1) creation of a socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2) try to connect to the server:
try:
    mySocket.connect((HOST, PORT))

except socket.error:
    print("Connexion has failed.")
    sys.exit()
print("Connected to the server.")

# 3) Interacts with the server:
msgClient = "GET /" + sys.argv[2] + " HTTP/1.0"
print(msgClient)
mySocket.send(msgClient.encode("Utf8"))

# Paramétrage de l'audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# Débuter l'enregistrement et la lecture
with open('record.wav', 'wb') as f:
    firstReceipt = True
    while True:
        print('receiving data...')
        data = mySocket.recv(CHUNK)
        print('data=%s', data)
        # Vérification si données présentes
        if not data:
            if firstReceipt:
                print("Pas de données pour cette chanson.")
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
print('File recorded - connection closed')

# 4) Closing connexion :
print("\n Connexion closed.")
mySocket.close()
