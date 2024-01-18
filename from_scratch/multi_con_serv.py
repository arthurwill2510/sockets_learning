import types
import socket
import selectors

selector = selectors.DefaultSelector()
address = ('127.0.0.1', 63000)

def accept_wrapper(sock):
    latest_conn, addr = sock.accept()
    latest_conn.setblocking(False)
    data = types.SimpleNamespace(inb=b'', outb=b'', address=addr)
    selector.register(latest_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def service_client(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        incoming_data = sock.recv(1024)
        if incoming_data:
            print('Data received from' , data.address[0],':', data.address[1])
            data.inb += incoming_data
        else:
            selector.unregister(sock)
            sock.close()
            print('The client at' +  data.address + 'has been disconnected')

    if mask & selectors.EVENT_WRITE:
        outgoing_data = b'HERE 23'
        amt_bytes_sent = sock.send(outgoing_data)
        data.outb += outgoing_data
        print('Data sent to' , address[0], ':' ,address[1])
        print('Data', data.outb )

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.setblocking(False)
listening_socket.bind(address)
listening_socket.listen()
selector.register(listening_socket, selectors.EVENT_READ, data=None)

while True:
    events = selector.select(timeout=None)
    for event in events:
        key, mask = event
        if key.fileobj == listening_socket:
            accept_wrapper(key.fileobj)
        else:
            try:
                service_client(key, mask)
            except BlockingIOError:
                # Handle non-blocking operation exception
                pass