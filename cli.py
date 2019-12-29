import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        cmd = input("msg: > ")
        s.sendall(cmd.encode('ascii'))
        if cmd == "end":
            break

print('Received', repr(data))