
import pandas as pd;
import os;
from threading import Lock

mutex = Lock()
Users = {}
def register(c, name):
    # Check if name exists in 
    if Users.setdefault(name, None) == None:
        # register name to 
        content = {
            "chat file":"./storing/",
            "friend list": "./storing",
            # ... to be configured
        }
        mutex.acquire()
        
        Users[name] = content
        mutex.release()
    
    pass


def threaded(c):
    while True:
        data = c.recv(1024)
        data = data.decode('ascii')
        print("In: {}".format(data))
        if data == "end":
            c.close()
            break
        if "REGISTER" in data:
            data = data.replace("REGISTER ", "")
        if not data:
            c.close()
            break