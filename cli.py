import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        cmd = input("msg: > ")
        s.sendall(cmd.encode('ascii'))
        rep = s.recv(1000).decode('ascii')
        print(rep)
        if cmd == "end":
            break
