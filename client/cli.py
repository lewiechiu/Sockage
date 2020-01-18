import socket
import time
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000         # The port used by the server
filename = "evensouth.mp3"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall("LOGIN ZZZ".encode('ascii'))
    rep = s.recv(10000).decode('ascii')
    time.sleep(0.5)
    s.sendall("999".encode('ascii'))
    

    # s.sendall("GETMSG abc".encode('ascii'))
    # rep = s.recv(10000).decode('ascii')
    # time.sleep(0.5)
    # while True:
    #     s.sendall("GETMSG gg".encode('ascii'))
    #     # rep = s.recv(10000).decode('ascii')
    #     time.sleep(0.5)
    #     # s.sendall(cmd.encode('ascii'))
    #     # rep = s.recv(10000).decode('ascii')
    #     s.sendall("""SEND Lewie I'd like to, "here" you go. """.encode('ascii'))
    #     time.sleep(0.5)
    #     rep = s.recv(10000).decode('ascii')
    #     input()
    #     print(rep)
    #     # if cmd == "end":
    #     #     break

    #### Tes