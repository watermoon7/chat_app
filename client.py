import socket, threading, utils, sys, time, re
from tkinter import messagebox
from tkinter import *

msg_list = ''
PORT = 5056
SERVER = '127.0.0.1'
NAME = ''
failed_connections = 0
client = None
STATE = 'CLOSED'

def connect():
    global client, STATE
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    utils.send(client, NAME)
    STATE = 'CONNECTED'

def check_details():
    global NAME, SERVER, PORT, failed_connections
    
    NAME = name_entry.get() if name_entry.get() not in [None, ""] and len(name_entry.get()) < 24 else None
    SERVER = ip_entry.get() if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip_entry.get()) else None
    PORT = int(port_entry.get()) if port_entry.get().isdigit() else None
    
    if all(i != None for i in [NAME, SERVER, PORT]):
        try:
            connect()
            root.destroy()
        except:
            failed_connections += 1
            error_label.config(text=f'Failed to connect {failed_connections} times')
    else:
        msg = []
        if not NAME:
            msg.append('Name too long or invalid name')
        if not SERVER:
            msg.append('Invalid IP')
        if not PORT:
            msg.append('Invalid PORT')
        
        error_label.config(text=', '.join(msg))
   
# login details
root = Tk()
root.geometry("400x150")
root.title("Chat Client")

root.columnconfigure(1, weight=1)

name_label = Label(root, text='Name')
name_label.grid(row=0, column=0)
name_entry = Entry(root)
name_entry.grid(row=0, column=1, sticky='ew')

ip_label = Label(root, text='IP')
ip_label.grid(row=1, column=0)
ip_entry = Entry(root)
ip_entry.grid(row=1, column=1, sticky='ew')
ip_entry.insert(0, '127.0.0.1')

port_label = Label(root, text='Port')
port_label.grid(row=2, column=0)
port_entry = Entry(root)
port_entry.grid(row=2, column=1, sticky='ew')
port_entry.insert(0, '5056')

error_label = Label(root, text='')
error_label.grid(row=3, column=1)

name_button = Button(root, text='Submit', command=check_details)
name_button.grid(column=1)

root.mainloop()
# end of login

DC_MESSAGE = '/dc'


def update_chat():
    global msg_list
    
    textbox.config(state=NORMAL)
    textbox.delete('1.0', END)
    textbox.insert('1.0', msg_list)
    textbox.see(END)
    textbox.config(state=DISABLED)

    
def get_text(event=None):
    global msg_list

    new = entry.get()
    if new != '': 
        utils.send(client, new)
    entry.delete(0, END)

    
def recieving_feed(client):
    global msg_list, STATE
    
    recieving = True
    while recieving:
        msg_list = utils.recieve(client)
        
        if msg_list in [DC_MESSAGE, None]:
            msg_list = "You have been disconnected. Restart the program to rejoin."
            root.unbind("<Return>")
            button["state"] = DISABLED
            
            STATE = 'CLOSED'
            recieving = False
            
        update_chat()

        
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        if STATE == 'CONNECTED':
            utils.send(client, '/dc')


            

# main loop
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

threading.Thread(target=recieving_feed, args=[client]).start()
root.mainloop()
