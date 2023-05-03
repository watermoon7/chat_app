import socket, utils, sys, time, re
from tkinter import messagebox
from tkinter import *

try:
    with open('details.txt', 'r') as f:
        NAME, PORT, SERVER = f.read().split(',')
except:
    NAME = ''
    PORT = 5056
    SERVER = '127.0.0.1'

msg_list = ''
failed_connections = 0
client = None
STATE = 'CLOSED'

def connect():
    global client, STATE
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    utils.send(client, NAME)
    STATE = 'CONNECTED'

def save(NAME, PORT, SERVER):
    with open('details.txt', 'w') as f:
        f.write('{},{},{}'.format(NAME, PORT, SERVER))

def check_details(event=None):
    global NAME, SERVER, PORT, failed_connections
    
    NAME = name_entry.get() if name_entry.get() not in [None, ""] and len(name_entry.get()) < 24 and all(char not in name_entry.get() for char in ',/ "\'') else None
    SERVER = ip_entry.get() if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip_entry.get()) else None
    PORT = int(port_entry.get()) if port_entry.get().isdigit() else None

    SAVE = save_variable.get()
    
    if all(i != None for i in [NAME, SERVER, PORT]):
        if SAVE:
            save(NAME, PORT, SERVER)
        try:
            connect()
            root.destroy()
        except:
            failed_connections += 1
            error_label.config(text='Failed to connect {} times'.format(failed_connections))
    else:
        msg = []
        if not NAME:
            msg.append('Name too long or invalid name')
        if not SERVER:
            msg.append('Invalid IP')
        if not PORT:
            msg.append('Invalid PORT')
        
        error_label.config(text=', '.join(msg))


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        sys.exit()

root = Tk()
root.geometry("400x150")
root.title("Chat Client")

root.columnconfigure(1, weight=1)

save_variable = IntVar()
save_checkbox = Checkbutton(root, text='Save Details', variable=save_variable)
save_checkbox.grid(row=3, column=0)

name_label = Label(root, text='Name')
name_label.grid(row=0, column=0)
name_entry = Entry(root)
name_entry.grid(row=0, column=1, sticky='ew')
name_entry.insert(0, NAME)

ip_label = Label(root, text='IP')
ip_label.grid(row=1, column=0)
ip_entry = Entry(root)
ip_entry.grid(row=1, column=1, sticky='ew')
ip_entry.insert(0, SERVER)

port_label = Label(root, text='Port')
port_label.grid(row=2, column=0)
port_entry = Entry(root)
port_entry.grid(row=2, column=1, sticky='ew')
port_entry.insert(0, str(PORT))

error_label = Label(root, text='')
error_label.grid(row=4, column=1)

name_button = Button(root, text='Submit', command=check_details, pady=10, padx=15)
name_button.grid(row=3, column=1)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Return>", check_details)

root.mainloop()
