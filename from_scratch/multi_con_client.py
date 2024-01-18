import types
import socket
import selectors

sel = selectors.DefaultSelector()

target_address = ('127.0.0.1', 49000)

for connid in range(5):
    connid += 1
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)
    client_socket.connect_ex(target_address)
    data = types.SimpleNamespace(inb=b'', outb=b'This is the message that I want the server to receive. JUST TESTING', target_addr=target_address, connid=connid)
    sel.register(client_socket, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

while True:
    events = sel.select(timeout=1)
    for event in events:
        key, mask = event
        sock =key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.inb += recv_data
                print('The client', data.connid ,'has recieved the data')
                print('Data', data.inb.decode('utf-8'))

        if mask & selectors.EVENT_WRITE:
            if data.inb:
                amt_bytes_sent = sock.send(data.outb)
                print('The client', data.connid ,'has sent' , amt_bytes_sent , 'amount of bytes')
                print('The client', data.connid ,'has been disconnected')
                sel.unregister(sock)
                sock.close()

    if not sel.get_map():
            break