import socket
import time
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000         # The port used by the server
filename = "evensouth.mp3"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall("LOGIN Lewie\n".encode('ascii'))
    time.sleep(0.5)
    s.sendall("9987\n".encode('ascii'))
    time.sleep(0.5)
    # s.sendall("GET ZZZ".encode('ascii'))
    # while True:
    #     s.sendall("GET Lewie".encode('ascii'))
    #     # s.sendall(cmd.encode('ascii'))
    #     rep = s.recv(10000).decode('ascii')
    #     s.sendall("""SEND Lewie I'd like to, "here" you go. """.encode('ascii'))
    #     rep = s.recv(10000).decode('ascii')
    #     input()
    #     print(rep)
    #     # if cmd == "end":
    #     #     break

    ##### Test sending files.
    # rep = s.recv(10000).decode('ascii')
    # print(rep)
    # s.sendall("SENDFILE ZZZ\n".encode('ascii'))
    # time.sleep(0.5)
    # rep = s.recv(10000).decode('ascii')
    # print(rep)
    # time.sleep(0.5)
    # s.sendall("{}".format(filename).encode('ascii'))
    # f = open("{}".format(filename), "rb")
    # l = f.read(1000)
    # while l:
    #     s.sendall(l)
    #     l = f.read(1000)
    # s.sendall(b'END')
    # time.sleep(1)
    # print("done sending")
    # rep = s.recv(10000).decode('ascii')
    # print(rep)
    ##### Close

    ##### GETFILE
    s.sendall("GETFILE".encode('ascii'))

    s.close()
