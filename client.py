import socket
import json
import os
import time

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    os.system("cls")
    print("Connected to server")
    print("=====>MENU<=====")
    print("1. Huffman")
    print("2. Shannon")
    menu = input("Choose menu : ")  # take input    

    while menu != 'exit()':
        if menu == "1":
            filename = input("Input txt file : ")  # take input
            if filename.lower().strip() == 'exit()':
                break
            send = json.dumps({"filename": filename, "menu": menu})
            client_socket.send(send.encode())  # send message

            data = client_socket.recv(4096)  # receive response
            data = json.loads(data.decode())
            com = data.get("a")
            dec = data.get("b")
            print('Compressed path : ' + com)  # show in terminal
            print('Decompressed path : ' + dec)  # show in terminal
            time.sleep(2)
            input("Press enter to continue ...")
        elif menu == "2":
            filename = input("Input image file : ")  # take input
            if filename.lower().strip() == 'exit()':
                break
            send = json.dumps({"filename": filename, "menu": menu})
            client_socket.send(send.encode())  # send message
            data = client_socket.recv(4096)  # receive response

            while data != "Done":
                data = client_socket.recv(4096).decode()  # receive response               
                print('Desponse from server : ' + data)  # show in terminal

            input("Press enter to continue ...")
        else:
            print('input invalid')
        os.system("cls")
        print("=====>MENU<=====")
        print("1. Huffman")
        print("2. Shannon")
        menu = input("Choose menu : ")  # take input      


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
