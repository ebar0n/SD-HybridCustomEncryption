#!/usr/bin/env python3
import os


def get_port():
    while True:
        try:
            port = int(input('Puerto (1024 - 49151): '))
            if port >= 1024 and port <= 49151:
                break
        except Exception:
            pass
    return port


def get_secure():
    type = input('Establecer conexion segura? S/N: ')
    return True if type in ['s', 'S'] else False

if __name__ == '__main__':
    os.system('clear')
    while True:
        print('1. Servidor')
        print('2. Cliente')
        type = input('Opcion: ')
        if type in ['1', '2']:
            break
        else:
            os.system('clear')
    os.system('clear')
    if type == '1':
        # Servidor
        print('Servidor')
        from server import init
        init(get_port())
    else:
        # Cliente
        ip = input('Ip del Servidor: ')
        from client import init
        init(ip, get_port(), get_secure())
