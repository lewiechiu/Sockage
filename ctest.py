import socket
import ssl
import getSSL
HOST = '127.0.0.1'
PORT = 7123



c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ec = getSSL.getCliSSL(c)
ec.connect((HOST,PORT))


print(ec.recv(5))
ec.close()


