import json
import socket
from datetime import datetime

from lib.settings import PATH_RECEIVE
from lib.utils import MyAsymmetric, _print, receive, receiveEncryptSymmetricKey, send, sendEncryptSymmetricKey


def init(ip, port, SECURE):
    try:
        request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        request.connect((ip, port))

        send(request, json.dumps({'SECURE': SECURE}).encode('UTF-8'))

        myAsymmetric = None
        if SECURE:
            myAsymmetric = MyAsymmetric()
            myAsymmetric.setPubFriend(json.loads(receive(request).decode('UTF-8')))
            send(request, json.dumps(myAsymmetric.getPub()).encode('UTF-8'))

            SYMMETRIC_KEY = int(myAsymmetric.decryptingAsymmetric(receive(request).decode('UTF-8')))
            _print('Clave simetrica recibida: {}'.format(SYMMETRIC_KEY))

        if SECURE:
            resp = receiveEncryptSymmetricKey(request, SYMMETRIC_KEY).decode('UTF-8')
        else:
            resp = receive(request).decode('UTF-8')

        files = json.loads(resp)
        for i in range(0, len(files)):
            _print('{}: {}'.format(i, files[i]))
        file = input('Archivo a descargar: ')

        if SECURE:
            sendEncryptSymmetricKey(request, file.encode('UTF-8'), SYMMETRIC_KEY)
        else:
            send(request, file.encode('UTF-8'))

        file_name = files[int(file)]
        file = open(PATH_RECEIVE + '/' + str(datetime.today()) + ' ' + file_name, 'wb')

        _print('Recibiendo archivo: {}'.format(file_name))
        while True:
            if SECURE:
                resp = receiveEncryptSymmetricKey(request, SYMMETRIC_KEY)
            else:
                resp = receive(request)
            if resp:
                file.write(resp)
            else:
                break
        file.close()
        _print('Archivo enviado con éxito')

    except KeyboardInterrupt:
        pass
    request.close()
