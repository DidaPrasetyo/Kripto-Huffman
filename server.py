import huffman, shannon
import socket
import json
import time


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server started, waiting for connection ...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(4096)
        if not data:
            # if data is not received break
            break
        data = json.loads(data.decode())
        menu = data.get("menu")
        if menu == "1":
            huff = data.get("filename") + ".txt"
            print("Process Huffman start")
            h = huffman.HuffmanCoding(huff)
            time.sleep(2)
            output_path = h.compress()
            decom_path = h.decompress(output_path)

            send = json.dumps({"a": output_path, "b": decom_path})
            conn.send(send.encode())
            time.sleep(2)
            print("Process done, waiting for next input")
        elif menu == "2":
            shann = data.get("filename")
            print("Process Shannon start")
            s = shannon.main(shann, conn)

            if s == "Done":
                conn.send(s.encode())

            print("Process done, waiting for next input")

    print("Client disconnected, Server terminated")
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
