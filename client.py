import socket, threading, utils
from tkinter import *

PORT = 5050
DC_MESSAGE = '/dc'
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

name = input('Name: ')
utils.send(client, name)

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
    if new != '': utils.send(client, new)
    entry.delete(0, END)

def recieving_feed(client):
    import time
    time.sleep(1)
    global msg_list
    while True:
        msg_list = utils.recieve(client)
        update_chat()
        

msg_list = ''

threading.Thread(target=recieving_feed, args=[client]).start()

root = Tk()
root.title("Tk example")
root.geometry("500x500")

button = Button(root, text="Send", command=get_text)
button.pack()

entry = Entry(root)
entry.pack()

textbox = Text(root)
textbox.config(state=DISABLED)
textbox.pack()

root.bind("<Return>",get_text)

root.mainloop() 
