import socket
from threading import *
import time

#Vector of clients
clients = []

#Set the connection variables
ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
port = 1234

#Server object
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Bind the selected port to this process
server_socket.bind( (ip,port) )

#Accept packets
server_socket.listen(25)
print("Server is running...")

#Send message to all clients except the sender
def broadcast(message):
    for client in clients:
        client.sendall(message)

#Manage of data that comes to the server
def serviClient(client_socket):
    name = client_socket.recv(100)
    broadcast(r"<< %s entered the chat room! >>" % (name))
    #print("<< %s entered the chat room! >>" % (name))
    while True:
        message = client_socket.recv(100)
        if message == 'exit()':
            clients.remove(client_socket)
            broadcast(r"<< %s left the chat room! >>" % (name))
            #print("<< %s left the chat room! >>" % (name))
            break
        else:
            broadcast(r"%s: %s" % (name, message))
            #print("%s: %s" % (name, message))
    time.sleep(1)
    client_socket.close()

#Accepting new client
while True:
    client_socket,client_ip = server_socket.accept()
    if client_socket:
        clients.append(client_socket)
        Thread(target = serviClient, args = (client_socket,)).start()
