import socket
import time
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall("LOGIN Lewie\n".encode('ascii'))
    time.sleep(0.5)
    s.sendall("9987\n".encode('ascii'))
    time.sleep(0.5)
    # s.sendall("GET ZZZ".encode('ascii'))
    while True:
        s.sendall("GET ZZZ".encode('ascii'))
        time.sleep(1.5)
        # s.sendall(cmd.encode('ascii'))
        rep = s.recv(10000).decode('ascii')
        s.sendall("""SEND ZZZ I am pleased to say so """.encode('ascii'))
        rep = s.recv(10000).decode('ascii')
        print(rep)
        # if cmd == "end":
        #     break
