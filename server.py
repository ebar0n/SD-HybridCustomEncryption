import json
import os
import threading
import time
import uuid

import socketserver
from lib.settings import PACKET_SIZE, PATH_SEND, TIME_SLEE
from lib.utils import MyAsymmetric, _print, receive, receiveEncryptSymmetricKey, send, sendEncryptSymmetricKey


class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class MyTCPServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        _print('Nuevo cliente...')

        resp = json.loads(receive(self.request).decode('UTF-8'))
        SECURE = resp.get('SECURE')

        if SECURE:
            send(self.request, json.dumps(myAsymmetric.getPub()).encode('UTF-8'))
            myAsymmetric.setPubFriend(json.loads(receive(self.request).decode('UTF-8')))

            SYMMETRIC_KEY = uuid.uuid4().int
            _print('Clave simetrica generada: {}'.format(SYMMETRIC_KEY))

            send(self.request, str(myAsymmetric.encryptAsymmetric(SYMMETRIC_KEY)).encode('UTF-8'))

        files = os.listdir(PATH_SEND)

        if SECURE:
            sendEncryptSymmetricKey(self.request, json.dumps(files).encode('UTF-8'), SYMMETRIC_KEY)
        else:
            send(self.request, json.dumps(files).encode('UTF-8'))

        if SECURE:
            resp = receiveEncryptSymmetricKey(self.request, SYMMETRIC_KEY).decode('UTF-8')
        else:
            resp = receive(self.request).decode('UTF-8')

        file_name = files[int(resp)]
        _print('Preparando para enviar {}'.format(file_name))

        file = open(PATH_SEND+'/'+file_name, 'rb')
        _print('Enviando archivo: {}'.format(file_name))
        while True:
            read = file.read(PACKET_SIZE)
            if not read:
                break
            if SECURE:
                sendEncryptSymmetricKey(self.request, read, SYMMETRIC_KEY)
            else:
                send(self.request, read)
            time.sleep(TIME_SLEE)
        file.close()
        _print('Archivo enviado con éxito\n\n')

    def handle_timeout(self):
        pass


def init(port):
    try:
        server = MyTCPServer(('0.0.0.0', port), MyTCPServerHandler)
        server_thread = threading.Thread(target=server.serve_forever)

        global myAsymmetric
        myAsymmetric = MyAsymmetric()
        server_thread.daemon = True
        server_thread.start()

        while True:
            time.sleep(TIME_SLEE + 2)

    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
