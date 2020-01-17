import socket
import pandas as pd
from _thread import *
import selectors
from threaded import *
from threading import Lock
from server import server



if __name__ == "__main__":

    # On starting, it should go through the harddisk storage.


    SERVER = server("./storing/Accounts.csv")
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servSocket.bind(('localhost', 8000))

    s = servSocket.listen(10)
    while 1:
        conn, addr = servSocket.accept()
        print ("New connection from IP: {}, Port: {}".format(addr[0], addr[1]))
        start_new_thread(threaded, (conn, SERVER ) )
        