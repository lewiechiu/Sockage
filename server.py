#us
import socket
import pandas as pd
from _thread import *
import selectors
from threaded import *
import json
import csv
import os

class server:
    def __init__(self, path_user):
        Users = set()
        self.users = Users
        self.OnlineUsers = set()
        tmp = pd.read_csv(path_user).values
        for i in tmp:
            Users.add(i[0])
            if i[3] == 1:
                self.OnlineUsers.add(i[0])
        print("Current Registered Users ", self.users)
        print("Online User: ", self.OnlineUsers)
    def Register(self, name, pwd):
        if name in self.users:
            return False
        else:
            # print(name, pwd)
            df = pd.read_csv("./storing/Accounts.csv")
            col = df.columns
            df_t = pd.DataFrame([[name, hash(pwd), "140.112.106.88", 0]], columns=col)
            df = df.append(df_t, ignore_index=True)
            df.to_csv("./storing/Accounts.csv", index=False)
            print("Currently Registered Clients")
            print(df)
            self.users.add(name)
            return True
    
    # Query if the "name" is in users
    def GetClient(self, name):
        return name in self.users
    def IsClientOnline(self, name):
        return name in self.OnlineUsers
    def isLoggedIn(self, name):
        df = pd.read_csv("./storing/Accounts.csv")
        for i in range(len(df.active)):
            if df.Username[i] == name:
                if df.active[i] == 1:
                    return True
                return False
    
    def Login(self, name, pwd):
        print(name, pwd)
        df = pd.read_csv("./storing/Accounts.csv")
        can_login = False
        for i in range(len(df.active)):
            if df.Username[i] == name and df.active[i] == 0:
                if df.hashed_pwd[i] == hash(pwd):
                    df.active[i] = 1
                    can_login = True
                    break
        if can_login == False:
            return can_login
        df.to_csv("./storing/Accounts.csv", index=False)
        print("User: {} Logged in!".format(name))
        self.OnlineUsers.add(name)
        # Check if the pwd matches the pwd of registered name.
        return True
    def GetChat(self, name, recv, whoami):
        print("getting chat {} {}".format(name, recv))
        chat = []
        print(os.listdir('./storing/chatroom/'))
        if "{}_{}.csv".format(name, recv) not in os.listdir('./storing/chatroom/'):
            df = pd.DataFrame(columns= ["No","Sender","msg","A_read","B_read"])
            df.to_csv("./storing/chatroom/{}_{}.csv".format(name, recv), index=False)
            return json.dumps([])
        df = pd.read_csv("./storing/chatroom/{}_{}.csv".format(name, recv))
        print(df)
        for i in df.values:
            chat.append({
                "msg": i[2],
                "sender": i[1],
                name : i[3],
                recv : i[4]})
        chat = json.dumps(chat)
        pos = 3
        if whoami == recv:
            pos = 4
        for i in range(len(df.values)):
            df.iloc[i, pos] = 1
        df.to_csv("./storing/chatroom/{}_{}.csv".format(name, recv), index=False, quoting=csv.QUOTE_NONNUMERIC)
        return chat
    def UpdateChat(self, name, recv, whoami, message):
        df = pd.read_csv("./storing/chatroom/{}_{}.csv".format(name, recv))
        print("Message: {}".format(message))
        col = df.columns
        if len(df.values) > 0:
            last_NO = int(df.values[-1][0]) + 1
        else:
            last_NO = 1
        if whoami == name:
            insert_data = [[last_NO, whoami, message, 1, 0]]
        else:
            insert_data = [[last_NO, whoami, message, 0, 1]]
        df_t = pd.DataFrame(insert_data, columns=col)
        df = df.append(df_t, ignore_index=True)
        df.to_csv("./storing/chatroom/{}_{}.csv".format(name, recv), index=False, quoting=csv.QUOTE_NONNUMERIC)
        print(df.values)

        return 
    def Storefile(self):
        pass
    def Receivable(self, name):
        files = os.listdir('./')
        matching_files = []
        for i in files:
            if name in i:
                matching_files.append(i)
        return matching_files
    def GoOffline(self, name):
        df = pd.read_csv("./storing/Accounts.csv")
        for i in range(len(df.active)):
            if df.Username[i] == name and df.active[i] == 1:
                df.active[i] = 0
                break
        df.to_csv("./storing/Accounts.csv", index=False)
        print("User: {} Logged Out!".format(name))
        self.OnlineUsers.remove(name)
        # Check if the pwd matches the pwd of registered name.
        return True