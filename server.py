#us
import socket
import pandas as pd
from _thread import *
import selectors
from threaded import *


class server:
    def __init__(self, path_user):
        Users = set()
        self.users = Users

        tmp = pd.read_csv(path_user).values
        for i in tmp:
            Users.add(i[0])
        print("Current Registered Users ", self.users)
    def Register(self, name, pwd):
        if name in self.users:
            return False
        else:
            # print(name, pwd)
            df = pd.read_csv("./storing/Accounts.csv")
            col = df.columns
            df_t = pd.DataFrame([[name, pwd, "140.112.106.88", 1]], columns=col)
            df = df.append(df_t, ignore_index=True)
            df.to_csv("./storing/Accounts.csv", index=False)
            print("Currently Registered Clients")
            print(df)
            self.users.add(name)
            return True
    
    # Query if the "name" is in users
    def GetClient(self, name):
        return name in self.users
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
        for i in range(len(df.active)):
            if df.Username[i] == name and df.active[i] == 0:
                if str(df.hashed_pwd[i]) == pwd:
                    df.active[i] = 1
                    break
        df.to_csv("./storing/Accounts.csv", index=False)
        print("User: {} Loggen in!".format(name))
        # Check if the pwd matches the pwd of registered name.
        return True