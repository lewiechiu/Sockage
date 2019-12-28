import socket
import pandas as pd
servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servSocket.bind(('localhost', 8000))

servSocket.listen(10)

print(pd.read_csv("./Accounts.csv"))

df = pd.read_csv("./Accounts.csv")
df_ = pd.DataFrame(["lewie","6448469829751745978","140.112.107.210","1"], df.va)
pd.concat([df, ], axis= 1)