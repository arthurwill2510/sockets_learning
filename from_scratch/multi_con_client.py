import types
import socket
import selectors

sel = selectors.DefaultSelector()
address = ('127.0.0.1', 63000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)
client_socket.connect_ex(address)
events = selectors.EVENT_READ | selectors.EVENT_WRITE
data = types.SimpleNamespace(
    connid=1,
    msg_total=len(b'TESTING'),
    recv_total=0,
    messages=b'TESTING',
    outb=b"",
)
sel.register(client_socket, events, data=data)


while True:
    events = sel.select(timeout=1)
    for event in events:
        key, mask = event

        if mask & selectors.EVENT_READ:
            incoming_data = key.fileobj.recv(1024)
            if incoming_data:
                print('Data received from' + data.address)
                data.inb += incoming_data
                print('Data is:', incoming_data.decode('utf-8'))
                break
            else:
                sel.unregister(key.fileobj)
                key.fileobj.close()
                print('The client at' +  data.address + 'has been disconnected')

        if mask & selectors.EVENT_WRITE:
            outgoing_data = b'HERE 10'
            amt_bytes_sent = key.fileobj.send(outgoing_data)
            data.outb += outgoing_data
            print('Data sent to' , address[0], ':' ,address[1])
            print('Data', data.outb )
        
            