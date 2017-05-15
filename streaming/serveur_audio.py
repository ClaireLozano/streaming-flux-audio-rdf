# CODE SERVER AUDIO
# coding=utf-8

import socket

port = 60000
host = socket.gethostname()
CHUNK = 8192

while True:
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)

    print 'Server listening....'

    # Etablissement de la communication avec le client
    conn, addr = s.accept()

    # Vérification de la data reçu
    data = conn.recv(CHUNK)
    print('Server received', repr(data))

    # Début du stream
    filename = './webroot/beta.wav'
    f = open(filename, 'rb')
    l = f.read(CHUNK)
    while l:
        conn.send(l)
        print('Sent ', repr(l))
        l = f.read(CHUNK)
    f.close()

    # Envoi terminé
    conn.close()
    print('Done sending')
