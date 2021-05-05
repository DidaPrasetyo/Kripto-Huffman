from huffman import HuffmanCoding
import socket
import json


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
        data = data.get("filename") + ".txt"
        h = HuffmanCoding(data)

        output_path = h.compress()
        print("Compressed file path: " + output_path)

        decom_path = h.decompress(output_path)
        print("Decompressed file path: " + decom_path)

        send = json.dumps({"a": output_path, "b": decom_path})
        conn.send(send.encode())
        print("Process done, waiting for next input")

    print("Client disconnected, Server terminated")
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
