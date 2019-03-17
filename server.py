import socket
from threading import *
import time

#Vector of clients
clients = []

#Detect an local ip adress
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#Set the connection variables
ip = get_ip()
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
        client.sendall(message.encode('utf-8'))

#Manage of data that comes to the server
def serviClient(client_socket):
    name = client_socket.recv(100).decode('utf_8')
    broadcast("<< %s entered the chat room! >>" % (name))
    print("<< %s entered the chat room! >>" % (name))
    while True:
        message = client_socket.recv(100).decode('utf_8')
        if message == 'exit()':
            clients.remove(client_socket)
            broadcast("<< %s left the chat room! >>" % (name))
            print("<< %s left the chat room! >>" % (name))
            break
        else:
            broadcast("%s: %s" % (name, message))
            print("%s: %s" % (name, message))
    time.sleep(1)
    client_socket.close()

#Accepting new client
while True:
    client_socket,client_ip = server_socket.accept()
    if client_socket:
        clients.append(client_socket)
        Thread(target = serviClient, args = (client_socket,)).start()
