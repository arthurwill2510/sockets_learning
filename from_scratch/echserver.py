import types
import socket

address = ('127.0.0.1', 62000)

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.bind(address)
listening_socket.listen()


try:
    server_client_connection, address = listening_socket.accept()
    print(f"Connection established with {address}")
    while True:
        input_data = server_client_connection.recv(100)
        print('R: ' + input_data.decode('utf-8'))
        if input_data:
            server_client_connection.sendall(input('S: ').encode('utf-8'))
        else:
            print("Client disconnected")
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    server_client_connection.close()
    listening_socket.close()

