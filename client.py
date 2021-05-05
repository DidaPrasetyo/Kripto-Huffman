import socket
import json


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("Connected to server")

    filename = input("Input txt file : ")  # take input

    while filename.lower().strip() != 'exit()':
        send = json.dumps({"filename": filename})
        client_socket.send(send.encode())  # send message

        data = client_socket.recv(4096)  # receive response
        data = json.loads(data.decode())
        com = data.get("a")
        dec = data.get("b")
        print('Compressed path : ' + com)  # show in terminal
        print('Decompressed path : ' + dec)  # show in terminal

        filename = input("Input txt file : ")  # take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
