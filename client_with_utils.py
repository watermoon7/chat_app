import socket, threading, utils, sys, time
from tkinter import *
from tkinter import messagebox

PORT = 5055
DC_MESSAGE = '/dc'
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

HEADER = 1024
def send(connection, msg):
    message = msg.encode('utf-8')
    message_length = len(message)
    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (HEADER-len(send_length))
    connection.send(send_length)
    connection.send(message)

def recieve(connection):
    msg_length = connection.recv(HEADER).decode('utf-8')
    if msg_length:
        return connection.recv(int(msg_length)).decode('utf-8')
    else:
        return None

def update_chat():
    global textbox, msg_list
    textbox.config(state=NORMAL)
    textbox.delete('1.0', END)
    textbox.insert('1.0', msg_list)
    textbox.see(END)
    textbox.config(state=DISABLED)


def get_text(event=None):
    global entry, msg_list

    new = entry.get()
    if new != '': send(client, new)
    entry.delete(0, END)

def recieving_feed(client):
    global msg_list
    time.sleep(0.4)
    global msg_list

    while True:
        msg_list = recieve(client)
        print(msg_list)
        print(msg_list==None)
        if msg_list == None:
            msg_list = "You have been disconnected. Restart the program to rejoin."
            update_chat()
            break
        update_chat()

name = ''
def check_name():
    global name
    if name_entry.get() not in [None, ""] and len(name_entry.get()) < 24:
        name = name_entry.get()
        initial.destroy()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        try:
            send(client, '/dc')
        except:
            ...

initial = Tk()
initial.geometry("300x70")
initial.title("Name Please")

name_label = Label(initial, text='Name must be less than 24 characters')
name_label.pack(side=BOTTOM, pady=5)
name_entry = Entry(initial)
name_entry.pack(side=LEFT, padx=10, pady=5)
name_button = Button(initial, text='Submit', command=check_name)
name_button.pack(side=LEFT)

initial.mainloop()

msg_list = ''

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
send(client, name)

threading.Thread(target=recieving_feed, args=[client]).start()

root = Tk()
root.title("Chat Client")
root.geometry("600x450")
root.configure(background='gray92')

button = Button(root, text="Send", command=get_text)
button.pack(ipadx=10, ipady=10, pady=10)

entry = Entry(root)
entry.pack(fill=Y, padx=10)

textbox = Text(root)
textbox.config(state=DISABLED)
textbox.pack(padx=10, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Return>",get_text)
root.mainloop()

