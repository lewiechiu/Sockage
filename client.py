
import socket
import tkinter as tk
from tkinter import messagebox
import time
import threading
import functools
import queue as Queue

lock = threading.Lock()
username_lock = threading.Lock()
'''
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		mesg = input('mesg:').encode()
		s.sendall(mesg)
		data = s.recv(1024)
		print('Received', repr(data))'''

def SocketSetup():
	HOST = '127.0.0.1'  # The server's hostname or IP address
	PORT = 8000        # The port used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	return s

def ask_recv_file(sock):
    	#TODO 
	return 1
#def check_new_message(sock):

def chatwith(username,root):
	#try:
		#userinput = root.queue.get(0)
		#root.newmessage(userinput + '\n')
	global lock
	msg = 'GETMSG ' + username 
	lock.acquire()
	root.sock.sendall(msg.encode())
	reply = root.sock.recv(1024)
	lock.release()
	if reply == b'NOTEXIST':
		return 0
	else:
		#print('chatwith:', reply)
		root.clear_chat_text()
		root.newmessage(reply.decode() + '\n')
		return 1

	#except:
		#return 0
	#msg = 'LOGIN ' + username
	#sock.sendall(msg.encode())
	#reply = sock.recv(1024)
	'''
	if username == 'Bob':
		return 1
	else:
		return 0
	'''

def logout():
	#TODO send by tcp socket
	return 1

def login_username(username, sock):
	if ' ' in username:
		print('should not have space!')
		return 0
	msg = 'LOGIN ' + username
	sock.sendall(msg.encode())
	reply = sock.recv(1024)
	#TODO send by tcp socket
	if reply == b'HI':
		return 1
	else:
		print('login_username:',reply)
		return 0

def login_password(password, sock):
	msg = password
	sock.sendall(msg.encode())
	reply = sock.recv(1024)
	#TODO send by tcp socket
	if reply == b'WELCOME':
		return 1
	else:
		print('login_password:',reply)
		return 0

def register_username(username, sock):
	if ' ' in username:
		print('should not have space!')
		return 0
	msg = 'REGISTER ' + username
	sock.sendall(msg.encode())
	reply = sock.recv(1024)
	#TODO send by tcp socket
	if reply == b'YES':
		return 1
	else:
		print('register_username:',reply)
		return 0

def register_password(password, sock):
	msg = password
	sock.sendall(msg.encode())
	reply = sock.recv(1024)
	#TODO send by tcp socket
	if reply == b'GOODJOB':
		return 1
	else:
		print('register_password:',reply)
		return 0
def SendMessage(username, message, sock):
	msg = 'SENDMSG ' + username + ' ' + message
	lock.acquire()
	sock.sendall(msg.encode())
	reply = sock.recv(1024)
	lock.release()
	#reply = sock.recv()
def ChatNewMessage(root):
	try:
		userinput = root.queue.get(0)
		root.clear_chat_text()
		root.newmessage(userinput + '\n')
		#global lock
		#msg = 'ask new message'
		#lock.acquire()
		#root.sock.sendall(msg.encode())
		#reply = root.sock.recv(1024)
		#time.sleep(0.4)
		#reply = b'test resp'
		#root.newmessage(reply.decode() + '\n')
		#lock.release()
	except:
		b = 9
	root.after(1000, ChatNewMessage, root)
	print('gs')

class RecvThread(threading.Thread):
	def __init__(self, queue, sock, root):
		threading.Thread.__init__(self)
		self.queue = queue
		self.sock = sock
		self.root = root
		self.cnt = 0
	def run(self):
		while True:
			if self.root.running != 1:
				break
			time.sleep(3)  # Simulate long running process
			#TODO
			#recv from scoket
			global lock, username_lock
			if self.root.chatting == 1:
				lock.acquire()
				username_lock.acquire()
				msg = 'GETMSG ' + self.root.username 
				self.sock.sendall(msg.encode())
				username_lock.release()
				reply = self.sock.recv(1024)
				lock.release()
				if reply == b'NOTEXIST':
					print('get error when routine check')
				else:
					self.queue.put(reply.decode())
				#print('chatwith:', reply)
			msg = 'GETFILE'
			lock.acquire()
			self.sock.sendall(msg.encode())
			reply = self.sock.recv(1024)
			if reply == b'NOFILES':
				pass
			else:
    			reply = reply.decode()
				parts = reply.split(' ')
				numoffile,a,filename = int(parts[0]),part[1],parts[2]
				reply = f'{a} {filename}'
				for i in range(numoffile):
    				_,filename = reply.split(' ')
    				f = open(filename, 'wb')
					self.sock.send(b'OK')
					reply = self.sock.recv(1000)
					while reply:
    					if b'END' in  reply:
							f.write(reply[:-3])
							break
						f.write(reply)
					self.sock.send(b'ACK')
					print(f'Success receive {filename}')
					f.close()
					if i+1 < numoffile:
						reply = self.sock.recv(1024)

			#self.queue.put(str(self.cnt))
			print('thread!')
			#self.cnt += 1
class ChatRoom(tk.Tk):
	def __init__(self, username, sock):
		super().__init__()
		self.username = username
		self.sock = sock
		self.queue = Queue.Queue()
		self.chatting = 0
		print('chatroom', self.sock)
		self.running = 1
		self.title(username)
		self.geometry('800x600')
		self.configure(background='black')
		self.loadmore = tk.Button(self, text='load more')
		self.loadmore.pack()

		self.scrollbar = tk.Scrollbar(self)
		self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
		self.chat = tk.Text(self, yscrollcommand=self.scrollbar.set, 
							background='gray15', fg='white',
							state="disabled")
		self.chat.pack(side=tk.RIGHT, fill=tk.BOTH)
		self.scrollbar.config(command=self.chat.yview)
		#mainapp
		self.username_label = tk.Label(self, text='username', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.username_label.pack()
		self.username_entry = tk.Entry(self)
		self.username_entry.pack()
		self.enterchatroom = tk.Button(self, text='chat', command=self.chatwith)
		self.enterchatroom.pack()
		#log out
		#enter chat room
		#send file
		self.messageframe = tk.Frame(self, background='black')
		self.messageframe.pack()
		self.msg = tk.Entry(self.messageframe)
		self.msg.pack(fill="none", expand=True, side=tk.LEFT)
		self.send = tk.Button(self.messageframe, text='send', command=self.sendmessage)
		self.send.pack(side=tk.LEFT)

		self.file_username_label = tk.Label(self, text='file receiver', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.file_username_label.pack()
		self.file_username_entry = tk.Entry(self)
		self.file_username_entry.pack()
		self.filename_label = tk.Label(self, text='file path', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.filename_label.pack()
		self.filename_entry = tk.Entry(self)
		self.filename_entry.pack()
		self.sendfile = tk.Button(self, text='sendfile')
		self.sendfile.pack()

		self.backtomain = tk.Button(self, text='logout', command=self.go_mainpage)
		self.backtomain.pack()
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		#self.sock.settimeout(5.0)
		self.recvthread = RecvThread(self.queue, self.sock, self)
		self.recvthread.start()
	def on_closing(self):
		self.running = 0
		self.recvthread.join()
		print('thread joined!')
		self.sock.settimeout(None)
		self.destroy()
		mainpage(self.sock)
	def newmessage(self, msg):
		if self.running == 1:
			self.chat.config(state="normal")
			self.chat.insert(1.0, msg)
			self.chat.config(state="disabled")
	def sendmessage(self):
		SendMessage(self.username, self.msg.get(), self.sock)
		self.msg.delete(0, 'end')
	def chatwith(self):
		username = self.username_entry.get()
		print("username:", username)
		username_lock.acquire()
		chatwith_success = chatwith(username, self)
		if chatwith_success == 1:
			#self.destroy()
			#chatroom(username, self.sock)
			self.chat.config(state="normal")
			#self.chat.delete('1.0', 'end')
			self.chat.config(state="disabled")
			self.username = username
			self.chatting = 1
			messagebox.showinfo(title='start chat', message='let\'s chat!')
		else:
			messagebox.showinfo(title='cannot chat!', message='no this user or not online')
		username_lock.release()
	def go_mainpage(self):
		logout()
		self.destroy()
		mainpage(self.sock)
	def send_file(self):
		print('send file')
	def clear_chat_text(self):
		self.chat.config(state="normal")
		self.chat.delete('1.0', 'end')
		self.chat.config(state="disabled")

'''
class MainApplication(tk.Tk):
	def __init__(self, sock):
		super().__init__()
		self.sock = sock
		self.title('MSG OuO')
		self.geometry('800x600')
		self.configure(background='black')
		self.username_label = tk.Label(self, text='username', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.username_label.pack()
		self.username_entry = tk.Entry(self)
		self.username_entry.pack()
		self.enterchatroom = tk.Button(self, text='chat', command=self.chatwith)
		self.enterchatroom.pack()
		self.filename_label = tk.Label(self, text='file path', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.filename_label.pack()
		self.filename_entry = tk.Entry(self)
		self.filename_entry.pack()
		self.sendfile = tk.Button(self, text='sendfile')
		self.sendfile.pack()
		#log out
		#enter chat room
		#send file
		self.backtomain = tk.Button(self, text='logout', command=self.go_mainpage)
		self.backtomain.pack()
	def go_mainpage(self):
		logout()
		self.destroy()
		mainpage(self.sock)
	def chatwith(self):
		username = self.username_entry.get()
		print('username:', username)
		chatwith_success = chatwith(username, self.sock)
		if chatwith_success == 1:
			#self.destroy()
			chatroom(username, self.sock)
		else:
			messagebox.showinfo(title='cannot chat!', message='no this user or not online')

'''

class RegisterPage(tk.Tk):
	def __init__(self, sock):
		super().__init__()
		self.sock = sock
		print('register', self.sock)
		self.title('register')
		self.geometry('800x600')
		self.configure(background='black')
		self.username_label = tk.Label(self, text='username', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.username_label.pack()
		self.username_entry = tk.Entry(self)
		self.username_entry.pack()
		self.password_label = tk.Label(self, text='password', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.password_label.pack()
		self.password_entry = tk.Entry(self, show='*')
		self.password_entry.pack()
		self.sendrequest = tk.Button(self, text='register', command=self.send_request)
		self.sendrequest.pack()
		self.backtomain = tk.Button(self, text='back to main page', command=self.go_mainpage)
		self.backtomain.pack()
	def send_request(self):
		username_accept = register_username(self.username_entry.get(), self.sock)
		if username_accept != 1:
			messagebox.showinfo(title='username', message='username GG!')
		else:
			password_accept = register_password(self.password_entry.get(), self.sock)
			if password_accept != 1:
				messagebox.showinfo(title='password', message='password GG!')
			else:
				messagebox.showinfo(title='login', message='success')
				self.destroy()
				mainpage(self.sock)
	def go_mainpage(self):
		self.destroy()
		mainpage(self.sock)

class LoginPage(tk.Tk):
	def __init__(self, sock):
		super().__init__()
		self.sock = sock
		print('login', self.sock)
		self.title('login')
		self.geometry('800x600')
		self.configure(background='black')
		self.username_label = tk.Label(self, text='username', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.username_label.pack()
		self.username_entry = tk.Entry(self)
		self.username_entry.pack()
		self.password_label = tk.Label(self, text='password', 
								background='black', 
								fg='white', 
								font=("Courier", 20))
		self.password_label.pack()
		self.password_entry = tk.Entry(self, show='*')
		self.password_entry.pack()
		self.sendrequest = tk.Button(self, text='login', command=self.send_request)
		self.sendrequest.pack()
		self.backtomain = tk.Button(self, text='back to main page', command=self.go_mainpage)
		self.backtomain.pack()
	def send_request(self):
		username_accept = login_username(self.username_entry.get(), self.sock)
		if username_accept != 1:
			messagebox.showinfo(title='username', message='username GG!')
		else:
			password_accept = login_password(self.password_entry.get(), self.sock)
			if password_accept != 1:
				messagebox.showinfo(title='password', message='password GG!')
			else:
				messagebox.showinfo(title='login', message='success')
				self.destroy()
				mainapplication(self.sock)

		#messagebox.showinfo(title='send_request', message='succeed')
	def go_mainpage(self):
		self.destroy()
		mainpage(self.sock)


class MainPage(tk.Tk):
	def __init__(self, sock):
		super().__init__()
		self.sock = sock
		print('mainpage', self.sock)
		self.title('MSG App')
		self.geometry('800x600')
		self.configure(background='black')
		#title
		self.header_label = tk.Label(self, text='my MSG', 
								background='black', 
								fg='white', 
								font=("Courier", 44))
		self.header_label.pack()
		#
		self.login_btn = tk.Button(self, text='login', 
							  font=("Courier", 40),
							  command=self.go_login,
							  width=10)
		self.login_btn.pack()
		self.register_btn = tk.Button(self, text='register', 
								 font=("Courier", 40),
								 command=self.go_register,
								 width=10)
		self.register_btn.pack()
	def go_login(self):
		self.destroy()
		login(self.sock)
	def go_register(self):
		self.destroy()
		register(self.sock)


def login_ask(a):
	if a%2 == 0:
		return 1
	else:
		return 1
'''
def chatroom(username, sock):

	chatr = ChatRoom(username, sock)
	chatr.after(1000, ChatNewMessage, chatr)
	chatr.mainloop()
	chatr.running = 0
'''

def login(sock):
	loginpage = LoginPage(sock)
	loginpage.mainloop()

def mainapplication(sock):
	#mainapplicationpage = MainApplication(sock)
	#mainapplicationpage.mainloop()
	username = 'OuO'
	chatr = ChatRoom(username, sock)
	chatr.after(1000, ChatNewMessage, chatr)
	chatr.mainloop()
	chatr.running = 0

def register(sock):
	registerpage = RegisterPage(sock)
	registerpage.mainloop()

def mainpage(sock):
	mainpagep = MainPage(sock)
	mainpagep.mainloop()
'''
window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('MSG App')
window.geometry('800x600')
window.configure(background='black')

#title
header_label = tk.Label(window, text='my MSG', 
						background='black', 
						fg='white', 
						font=("Courier", 44))
header_label.pack()

#
login_btn = tk.Button(window, text='login', 
					  font=("Courier", 40),
					  command=login, 
					  width=10)
login_btn.pack()
register_btn = tk.Button(window, 
						 text='register', 
						 font=("Courier", 40), 
						 width=10)
register_btn.pack()

# 運行主程式
window.mainloop()'''
socket1 = SocketSetup()
print(socket1)
mainpage(socket1)
#mainapplication(socket1)