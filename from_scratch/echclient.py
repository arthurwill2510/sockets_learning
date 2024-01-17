import types
import socket

address = ('127.0.0.1', 62000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)
input_d = input('S: ')

while True:
    if input_d:
        client_socket.sendall(input_d.encode('utf-8'))
        input_d = None
    elif not input_d:
        print('R: ' + client_socket.recv(100).decode('utf-8'))
        client_socket.sendall(input('S: ').encode('utf-8'))
    else:
        client_socket.close()
