import socket
import base64
import os
import ssl
import getSSL


HOST = '127.0.0.1'
PORT = 7123

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(5)
newsock, fromaddr = s.accept()
es = getSSL.getSrvSSL(newsock)
es.sendall(b'jizz')
es.close()