
import pandas as pd
import os
from server import server


MSG_SIZE = 1024
def threaded(c, SERVER):
    # This "Name" variable will be None before Logged In.
    Name = None
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
                c.send("NO, user: {} is already online".format(name).encode('ascii'))
                print("user : {} is already online".format(name))
                continue
            c.send("HI".encode('ascii'))
            pwd = c.recv(MSG_SIZE).decode('ascii')
            if SERVER.Login(name, pwd):
                c.send("Welcome!... Unread msgs:{}".format(3).encode("ascii"))
                Name = name
            else:
                c.send("GO AWAY".encode("ascii"))
        elif "GET" in data and Name != None:
            data = data.replace("GET ", "")
            if not SERVER.GetClient(data):
                c.send("User : {} NOTEXIST".format(data).encode('ascii'))
                return
            if data > Name:
                chat = SERVER.GetChat(Name, data, Name)
            else:
                chat = SERVER.GetChat(data, Name, Name)
            c.send(chat.encode("ascii"))
                
            pass
        elif "SEND" in data and Name != None:
            data = data.replace("SEND ", "")
            receiver = data.split(' ')[0]
            data = data.replace(receiver, "")
            data = data.replace(" ", "", 1)
            print(data)
            if not SERVER.GetClient(receiver):
                c.send("User: {} NOTEXIST".format(receiver).encode('ascii'))
                return
            if receiver > Name:
                SERVER.UpdateChat(Name, receiver, Name, data)
            else:
                SERVER.UpdateChat(receiver, Name, Name, data)
            c.send("DONE".encode('ascii'))