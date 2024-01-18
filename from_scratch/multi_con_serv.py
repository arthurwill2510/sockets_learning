import types
import socket
import selectors 

server_address = ('127.0.0.1', 49000)
sel = selectors.DefaultSelector()

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.setblocking(False)
listening_socket.bind(server_address)
listening_socket.listen()
sel.register(listening_socket, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    server_end_conn, address = sock.accept()
    server_end_conn.setblocking(False)
    print('We have now connected to the server at ', address[0] , ':' , address[1])
    data = types.SimpleNamespace(inb=b'', outb=b'', addr=address)
    sel.register(server_end_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def service_socket(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ: 
        try:
            recv_data = sock.recv(1024)
            if recv_data:
                print('We recieved Data from the client at', data.addr[0], ':' ,data.addr[1])
                data.inb += recv_data   
        except ConnectionResetError:
            key.fileobj.close()
            sel.unregister(key.fileobj)

    if mask & selectors.EVENT_WRITE:
        try:
            data.outb = b'THIS IS JUST A TEST ROUND TO SEE HOW THINGS WORK NOT TOO SURE ABOUT THIS YET'
            amt_bytes_sent = sock.send(data.outb) 
            print(amt_bytes_sent, 'Amount of bytes have been sent over to the client', data.addr[0], ':' ,data.addr[1])
        except (BrokenPipeError, OSError) as e:
            if e == BrokenPipeError:
                key.fileobj.close()
                sel.unregister(key.fileobj)
            else:
                sel.get_map == None



while True:
    events = sel.select(timeout=2)
    # try:
    for event in events:
        key, mask = event
        if key.data == None:
            accept_wrapper(key.fileobj)
        else:
            service_socket(key, mask)
        
    if not events:
            break
        