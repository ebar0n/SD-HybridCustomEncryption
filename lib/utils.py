import base64
import time
import uuid
from datetime import datetime

from lib.settings import PACKET_SIZE, TIME_SLEE


def _print(message):
    print('[{}] {}'.format(datetime.today(), message))


def send(request, message):
    _print('send: {}'.format(message))
    request.sendall(message)
    time.sleep(TIME_SLEE)


def receive(request):
    message = request.recv(PACKET_SIZE)
    _print('recv: {}'.format(message))
    time.sleep(TIME_SLEE)
    return message


def sendEncryptSymmetricKey(request, message, key):
    # _print('send: {}'.format(message))
    new_message = ''
    for a in base64.b64encode(message).decode('UTF-8'):
        b = ord(a)
        new_message += '{} '.format(key * b)
    new_message += '.'
    send(request, new_message.encode('UTF-8'))

global residue
residue = ''


def receiveEncryptSymmetricKey(request, key):
    global residue

    if residue:
        receive_message = residue
    else:
        receive_message = ''

    while True:
        receive_message += receive(request).decode('UTF-8')
        if receive_message.find(' .') > 0:
            receive_message = receive_message.split(' .')
            if len(receive_message) == 2:
                residue = receive_message[1]
            receive_message = receive_message[0]
            break
        if not receive_message:
            break

    if receive_message:
        message = ''
        for m in receive_message.split(' '):
            message += chr(int(int(m) / key))

        return base64.b64decode(message.encode('UTF-8'))
    else:
        return None


class MyAsymmetric:

    def __init__(self):
        super(MyAsymmetric, self).__init__()
        self.genereKeys()

    def genereKeys(self):
        p = uuid.uuid4().int
        q = uuid.uuid4().int
        r = p + q
        self.priv = {'p': p, 'r': r}
        self.pub = {'q': q, 'r': r}

    def getPub(self):
        return self.pub

    def setPubFriend(self, pub):
        self.pubFriend = pub

    def encryptAsymmetric(self, m):
        c = ''
        for l in str(m):
            b = ord(l)
            c += '{} '.format(b * self.pubFriend.get('q'))
        return base64.b64encode(c.encode('UTF-8')).decode('UTF-8')

    def decryptingAsymmetric(self, c):
        message = ''
        text = base64.b64decode(c.encode('UTF-8')).decode('UTF-8').split(' ')
        text.pop()
        for l in text:
            message += chr(int(int(l) / (self.priv.get('r') - self.priv.get('p'))))
        return int(message)
