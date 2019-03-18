import tkinter as tk
from tkinter import *
import socket
from threading import *

class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.title("L_Chat")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.socket = Socket()
        self.socket.start()
        self.frames = {}
        for F in (StartPage, ChatBox):
            page_name = F.__name__
            frame = F(parent=container, controller=self, socket = self.socket)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "ChatBox":
            frame.update_socket(self.socket)
            frame.start_thread()
        else:
            frame.update_socket(self.socket)


class StartPage(tk.Frame):

    def __init__(self, parent, controller, socket):
        tk.Frame.__init__(self, parent, bg="#121113")
        self.controller = controller

        def connect():
            ip = ip_field.get()
            port = port_field.get()
            name = name_field.get()
            try:
                self.client_socket.connect( (ip,int(port)) )
                self.client_socket.sendall(name.encode('utf-8'))
                err.set("")
                controller.show_frame("ChatBox")
                pass
            except:
                err.set("Connection cannot be established!")


        label1 = Label(self, text="Enter Server Ip & Port:",bg="#121113", fg="#EDECEF").pack(side="top", pady = 10)

        entry_frame = Frame(self, bg="#121113")
        ip_field = Entry(entry_frame, bg="#46434C", fg="#EDECEF")
        ip_field.pack(side="left", padx = 2.5)
        port_field = Entry(entry_frame, width = 5, bg="#46434C", fg="#EDECEF")
        port_field.pack(side="left", padx = 2.5)
        entry_frame.pack()

        label2 = Label(self, text="Enter Your Name:",bg="#121113", fg="#EDECEF").pack(pady = 10)

        name_field = Entry(self, bg="#46434C", fg="#EDECEF")
        name_field.pack()

        err = StringVar()
        err_label = Label(self, textvariable=err,bg="#121113", fg="#D92700").pack(pady = 10)

        button1 = Button(self, text="Connect", bg="#46434C", fg="#EDECEF",
                        command = lambda: connect())
        button1.pack(side=BOTTOM, fill=X)

    def update_socket(self, socket):
        self.client_socket = socket.get_socket()

class ChatBox(tk.Frame):

    def __init__(self, parent, controller, socket):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def disconnect():
            dis = "exit()"
            self.client_socket.sendall(dis.encode('utf-8'))
            self.client_socket.close()
            self.controller.socket.start()
            controller.show_frame("StartPage")
            self.messages.configure(state='normal')
            self.messages.delete(1.0,END)
            self.messages.configure(state='disabled')

        def send_message(event):
            message = input_field.get()
            if message != '' and message != 'exit()':
                self.client_socket.sendall(message.encode('utf-8'))
            input_user.set('')
            return "break"

        button = tk.Button(self, text="Disconnect", bg="#46434C", fg="#EDECEF",
                           command=lambda: disconnect())
        button.pack(fill=X)

        self.messages = Text(self,state='disabled', bg="#121113", fg="#EDECEF")
        self.messages.pack(fill=BOTH,expand=1)

        input_user = StringVar()
        input_field = Entry(self, text=input_user, bg="#121113", fg="white")
        input_field.pack(side=BOTTOM, fill=X)
        input_field.bind("<Return>", send_message)

    def start_thread(self):
        Thread(target = self.chatThread).start()

    def chatThread(self):
        while True:
            try:
                message = self.client_socket.recv(100).decode('utf_8')
                self.messages.configure(state='normal')
                self.messages.insert(INSERT, '%s\n' % message)
                self.messages.configure(state='disabled')
            except:
                break


    def update_socket(self, socket):
        self.client_socket = socket.get_socket()

class Socket():
    # def __init__(self):
    #     self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def start(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def get_socket(self):
        return self.client_socket
    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
