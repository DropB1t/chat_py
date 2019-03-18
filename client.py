import socket
from threading import *
import time
import os
import sys

#Clean the console screen (Windows = cls / Linux = clear)
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

def newName():
	name = input('Please enter your name--> ')
	return name.encode('utf-8')

def chatThread(client_socket):
	while True:
		try:
			message = client_socket.recv(100).decode('utf_8')
		except:
			break
		print(message)


#Set the connection variables
#ip = '192.168.1.3'
ip = input("Enter the server ip--> ")
port = 1234

#Create socket object
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Connect to the server
try:
	client_socket.connect( (ip,port) )
except:
	print("Connection cannot be established!")

client_socket.sendall(newName())

clear()
print("Write 'exit()' to quit the chat")
#Start receiving data from server (Other clients)
Thread(target = chatThread, args = (client_socket,)).start()

#Send the data to the server
while True:
	message = input()
	sys.stdout.write('\x1b[1A') #CURSOR_UP_ONE
	sys.stdout.write('\x1b[2K') #ERASE_LINE
	client_socket.sendall(message.encode('utf-8'))
	if message == 'exit()':
		client_socket.close()
		break
