
import pandas as pd
import os
from server import server


MSG_SIZE = 1024
def threaded(c, SERVER):
    while True:
        data = c.recv(MSG_SIZE)
        data = data.decode('ascii')
        if not data:
            print("Connection ended by user")
            c.close()
            break
        print("In: {}".format(data))
        if data == "end":
            c.close()
            break
        if "REGISTER" in data:
            name = data.replace("REGISTER ", "")
            name = name.replace('\n', "")
            if SERVER.GetClient(name):
                c.send("No".encode('ascii'))
                print("user Exists")
                continue
            else:
                c.send("Yes".encode('ascii'))
            pwd = c.recv(MSG_SIZE).decode('ascii')
            pwd = pwd.replace('\n', "")
            if SERVER.Register(name, pwd):
                c.send("GOODJOB".encode('ascii'))
            else:
                c.send("FAIL".encode('ascii'))
        elif "LOGIN" in data:
            name = data.replace("LOGIN ", "")
            name = name.replace('\n', "")
            print(name)
            if not SERVER.GetClient(name):
                c.send("NO".encode('ascii'))
                print("user DNE")
                continue
                
            if SERVER.isLoggedIn(name):
                c.send("NO, user is already online".encode('ascii'))
                print("user is already online")
                continue
            c.send("HI".encode('ascii'))
            pwd = c.recv(MSG_SIZE).decode('ascii')
            if SERVER.Login(name, pwd):
                c.send("Welcome!... Unread msgs:{}".format(3).encode("ascii"))
            else:
                c.send("GO AWAY".encode("ascii"))