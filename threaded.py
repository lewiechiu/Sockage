
import pandas as pd
import os
from server import server


MSG_SIZE = 1024

def receive(c):
    msg = c.recv(MSG_SIZE).decode('ascii')
    msg = msg.replace("\n", "")
    print("In: {}".format(msg))
    return msg

def threaded(c, SERVER):
    # This "Name" variable will be None before Logged In.
    Name = None
    while True:
        data = receive(c)
        if not data:
            print("Connection ended by user")
            c.close()
            break
        if data == "end":
            c.close()
            break
        if "REGISTER" in data:
            name = data.replace("REGISTER ", "")
            name = name.replace('\n', "")
            if SERVER.GetClient(name):
                c.send("NO".encode('ascii'))
                print("user Exists")
                continue
            else:
                c.send("YES".encode('ascii'))
            pwd = receive(c)
            print("Password: {}".format(pwd))
            pwd = pwd.replace('\n', "")
            if SERVER.Register(name, pwd):
                c.send("GOODJOB".encode('ascii'))
            else:
                c.send("FAIL".encode('ascii'))
        elif "LOGIN" in data:
            name = data.replace("LOGIN ", "")
            name = name.replace('\n', "")
            print("login user name: {}".format(name))
            if not SERVER.GetClient(name):
                c.send("NO".encode('ascii'))
                print("user DNE")
                continue
                
            if SERVER.isLoggedIn(name):
                c.send("NO, user: {} is already online".format(name).encode('ascii'))
                print("user : {} is already online".format(name))
                continue
            c.send("HI".encode('ascii'))
            pwd = receive(c)
            if SERVER.Login(name, pwd):
                c.send("WELCOME".encode("ascii"))
                Name = name
            else:
                c.send("GO AWAY".encode("ascii"))
        elif "GETMSG" in data and Name != None:
            data = data.replace("GETMSG ", "")
            if not SERVER.GetClient(data):
                c.send("NOTEXIST".encode('ascii'))
            else:
                if data < Name:
                    chat = SERVER.GetChat(Name, data, Name)
                else:
                    chat = SERVER.GetChat(data, Name, Name)
                c.send(chat.encode("ascii"))
        elif "SENDMSG" in data and Name != None:
            data = data.replace("SENDMSG ", "")
            receiver = data.split(' ')[0]
            data = data.replace(receiver, "")
            data = data.replace(" ", "", 1)
            print(data)
            if receiver < Name:
                SERVER.UpdateChat(Name, receiver, Name, data)
            else:
                SERVER.UpdateChat(receiver, Name, Name, data)
            c.send("DONE".encode('ascii'))
        elif "SENDFILE" in data and Name != None:
            data = data.replace("SENDFILE ", "")
            data = data.replace('\n','')
            print(data)
            if not SERVER.isLoggedIn(data):
                c.send("OFFLINE".format(data).encode('ascii'))
            else:
                c.send("OK".encode('ascii'))
                # Receives the filename and filesize
                filename = receive(c)
                c.send("OK".encode('ascii'))
                # Start to receive the file.
                print("file name: {}".format(filename))
                f = open("S_{}_{}".format(data, filename), "wb")
                fi = c.recv(1000)
                while fi:
                    print(fi)
                    if b'END' in fi:
                        f.write(fi[:-3])
                        break
                    # Make a loading bar here.
                    f.write(fi)
                    fi = c.recv(1000)
                    
                f.close()
                print("Finish receiving")
                c.send("DONE".encode('ascii'))
                
                
            
        elif "GETFILE" in data and Name != None:
            can_send = SERVER.Receivable(Name)
            if len(can_send) == 0:
                c.send("NOFILES".encode('ascii'))
            else:
                c.send(str(len(can_send)).encode('ascii'))
                resp = receive(c)
                for i in can_send:
                    filename = i.replace('S_', "")
                    c.send("SENDING {}".format(filename).encode('ascii'))
                    resp = receive(c)
                    
                    f = open("{}".format(i).encode('ascii'), "rb")
                    l = f.read(1000)
                    while l:
                        c.sendall(l)
                        l = f.read(1000)
                    c.sendall(b'END')
                    resp = receive(c)
                    os.remove(i)
        elif "LOGOUT" in data and Name != None:
            SERVER.GoOffline(Name)