# Command Line Messenger

## Register

Client sends:

```{code=python}
REGISTER <User Name><LF>
```

If name is registered, it returns

```{code=python}
No
```

else:

```{code=python}
Yes
```

If the client receives an **YES**, it will then send the passwd in following format.

```{code=python}
<PASSWORD><LF>
```

Server will then do some checking in the backend. If it passes the checking, it will return:

```{code=python}
GOODJOB
```

Otherwise, it will be one of the following

```{code=python}
INVALIDCHAR # Invalid character detected in the password string
TOOLONG # String too long for password
TOOSHORT # String too short for password
```

For server side, registered client file will have a file call

## File Storing Structure

### storing

* Accounts.csv: Records the User's *Name*, *password*, *IP*, *active state*.
* Chatroom.csv: Stores who (*name*) is in which chatroom(*RoomID*).
* ./chatroom/: Within this directory, file names are the ID that can be found in *Chatroom.csv*.
