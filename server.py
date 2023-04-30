import socket, threading, utils, commands, time, sys
from tkinter import ttk, messagebox
from tkinter import *

# SETTINGS -----
SERVER = '127.0.0.1'
PORT = 5055
ADDR = (SERVER, PORT)
STATE = 'CLOSED'
DISCONNECT_MESSAGE = "/dc"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# -----

clients = {}
msg_list = []

def update():
    for client in clients:
        utils.send(clients[client].connection, ''.join(msg_list))

    chat_box.config(state=NORMAL)
    chat_box.delete('1.0', END)
    chat_box.insert('1.0', ''.join(msg_list))
    chat_box.see(END)
    chat_box.config(state=DISABLED)

custom_messages = {
    'connection': lambda *args: f'| @{args[0]} has connected |\n',
    'kick':       lambda *args: f'| @{args[0]} has been kicked |\n',
    'dc':         lambda *args: f'| @{args[0]} has left |\n',
    'server':     lambda *args: f'[SERVER] {args[1]}\n' + (f'{commands.command(args[1])}\n' if args[1].split()[0] in commands.commands else ''),
    'default':    lambda *args: f'{args[0]} > {args[1]}\n' + (f'{commands.command(args[1])}\n' if args[1].split()[0] in commands.commands else '')
    }

def message(type_, name=None, msg=None):
    msg = custom_messages[type_](name, msg)
    msg_list.append(msg)
    update()

def disconnect(client):
    global clients
    clients[client].connected = False
    client_list.delete(list(clients.keys()).index(client))
    del clients[client]
    message('dc', client)

class Client():
    def __init__(self, connection, addr, name):
        self.connected = True
        self.connection = connection
        self.addr = addr
        self.name = name
    
    def run(self):
        while self.connected:
            msg = utils.recieve(self.connection)
            if msg == DISCONNECT_MESSAGE:
                disconnect(self.name)
            else:
                message('default', self.name, msg)
                    
        self.connection.close()
        
def client_handler():
    global clients
    server.listen()
    try:
        while STATE == 'OPEN':
            connection, addr = server.accept()
            name = utils.recieve(connection).strip()
            clients[name] = Client(connection, addr, name)
            client_list.insert(len(clients), name)
                
            threading.Thread(target=clients[name].run, args=()).start()
            message('connection', name)
    except Exception as e:
        print('Error has been detected at function "client_handler()"')
        print(e)

    
def start():
    global STATE
    
    def select_port():
        global PORT
        port_found = False
        while not port_found:
            try:
                server.bind(ADDR)
                port_found = True
            except:
                PORT += 1
                ADDR = (SERVER, PORT)
    
    STATE = 'OPEN'
    open_server["state"] = DISABLED
    
    select_port()
    root.title(f'IP: {SERVER}     Port: {PORT}')
    threading.Thread(target=client_handler, args=()).start()
    message('server', msg='SERVER STARTED')

def send_message(event=None):
    text = input_box.get()
    input_box.delete(0, END)

    message('server', msg=text)

def kick():
    selected_client = client_list.curselection()
    if selected_client != ():
        disconnect(client_list.get(selected_client))    

def disconnect_all():
    for client in clients.copy():
        disconnect(client)
    message('server', msg='DISCONNECTED ALL CLIENTS')

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        disconnect_all()
        server.close()
        root.destroy()

root = Tk()
root.title('Display Demo')
root.geometry('750x450')

root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

client_controls = Frame(root, width=150, height=400, padx=10, pady=10)
chat_controls = Frame(root, width=450, height=400, padx=10, pady=10)

client_controls.grid(row=0, column=0, sticky='ns')
client_controls.rowconfigure(0, weight=1)

chat_controls.grid(row=0, column=1, sticky='nsew')
chat_controls.columnconfigure(0, weight=1)
chat_controls.rowconfigure(0, weight=1)

# client widgets
client_list = Listbox(client_controls)
client_list.grid(row=0, sticky='ns')

kick_button = Button(client_controls, text='Kick', command=kick)
kick_button.grid(ipadx=3, ipady=3)

# chat widgets
chat_window_frame = Frame(chat_controls, width=450, height=250, padx=5, pady=5)
chat_window_frame.rowconfigure(0, weight=1)
chat_window_frame.columnconfigure(0, weight=1)
chat_input_frame = Frame(chat_controls, width=450, height=50, padx=5, pady=5)
chat_options_frame = Frame(chat_controls, width=450, height=100, padx=5, pady=5)

chat_window_frame.grid(row=0, column=0, sticky='nsew')
chat_input_frame.grid(row=1, sticky='nsew')
chat_options_frame.grid(row=2, sticky='nsew')

# chat window widgets
chat_box = Text(chat_window_frame, bg='gray93')
chat_box.grid(row=0, sticky='nsew')

# chat input widgets
chat_input_frame.columnconfigure(0, weight=1)
chat_input_frame.columnconfigure(1, weight=4)

input_button = Button(chat_input_frame, text='Send', command=send_message)
input_button.grid(row=0, column=0, sticky='ew', ipadx=3, ipady=3)

input_box = Entry(chat_input_frame)
input_box.grid(row=0, column=1, sticky='ew')

# chat options widgets
open_server = Button(chat_options_frame, text ='Open', command=start)
open_server.pack(side=RIGHT, ipadx=5, ipady=5, padx=3)

disconnect_all_button = Button(chat_options_frame, text ='Disconnect All Clients', command=disconnect_all)
disconnect_all_button.pack(side=RIGHT, ipadx=5, ipady=5, padx=3)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Return>", send_message) 
root.mainloop()
