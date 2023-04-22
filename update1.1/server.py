import socket, threading, utils, commands, time, sys
from tkinter import *
from tkinter import ttk, messagebox 

HEADER = 64
PORT = 5054
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "/dc"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg_list = []
clients = []

class Client():

    def __init__(self, connection, addr, name):
        self.connection = connection
        self.addr = addr
        self.name = name
            
        self.connected = True
        self.client_id = (self.connection, self.name)
        clients.append((connection, name))
        lst.insert(len(clients), name)


def update():
    for c in clients:
        utils.send(c[0], ''.join(msg_list))

    textbox.config(state=NORMAL)
    textbox.delete('1.0', END)
    textbox.insert('1.0', ''.join(msg_list))
    textbox.see(END)
    textbox.config(state=DISABLED)


custom_messages = {
    'connection': lambda name: f'| @{name} has connected |',
    'kick':       lambda name: f'| @{name} has been kicked |',
    'dc':         lambda name: f'| @{name} has left |',
    }

def message(name, type_=None, msg=None):
    if msg == "":
        return 
    if name == 'server':
        msg_list.append(f'[SERVER] {msg}\n')
        print(f'[SERVER] {msg}') 
        if msg != "" and msg.split()[0] in commands.commands:
            result = commands.command(msg)
            msg_list.append(f'{result}\n')
            print(f"{result}\n")
    elif type_ == None:
        msg_list.append(f" {name} > {msg}\n")
        print(f" {name} > {msg}")
    elif type_ == 'command':
        result = commands.command(msg)
        msg_list.append(f" {name} > {msg}\n")
        msg_list.append(f"{result}\n")
        print(f" {name} > {msg}")
        print(f"{result}")
    else:
        msg = custom_messages[type_](name)
        msg_list.append(f'{msg}\n')
        print(msg)
    update()
        
def get_text(*args):
    text = entry.get()
    entry.delete(0, END)

    message('server', msg=text)

    textbox.config(state=NORMAL)
    textbox.delete('1.0', END)
    textbox.insert('1.0', ''.join(msg_list))
    textbox.see(END)
    textbox.config(state=DISABLED)

def handle_client(client):
    print(f"[NEW CONNECTION] {client.name} at {client.addr} connected.")
    try:
        while True:
            msg = utils.recieve(client.connection)
            if msg == DISCONNECT_MESSAGE:
                message(client.name, 'dc')
                lst.delete(clients.index(client.client_id))
                break
            else:
                if msg.split()[0] in commands.commands:
                    message(client.name, 'command', msg)
                else:    
                    message(client.name, msg=msg)
    except:
        print("An Error occurd and {client.name} was disconnected")
        if client.client_id in clients: message(client.name, 'kick')
        try: lst.delete(clients.index(client.client_id))
        except: ...
        time.sleep(0.1)
        
    client.connection.close()
    if client.client_id in clients:
        clients.remove(client.client_id)
    

    print(f"[ACTIVE CONNECTIONS] {len(clients)}")


def kick_client():
    cli = lst.curselection()
    if cli == ():
        return
    
    connection = clients[[c[1] for c in clients].index(lst.get(cli))][0]
    connection.close()
    clients.remove((connection, lst.get(cli)))
    
    #message(lst.get(cli), 'kick')
    
    lst.delete(cli)

def new_client_handler():
    server.listen()
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")
    try:
        while True:
            connection, addr = server.accept()
            name = utils.recieve(connection).strip()
            client = Client(connection, addr, name)
            
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
            
            message(name, 'connection')
            print(f"[ACTIVE CONNECTIONS] {len(clients)}")
    except:
        print('Clients handeled')

def start():
    global server, PORT, SERVER
    s["state"] = DISABLED
    while True:
        try:
            server.bind(ADDR)
            print(f"[PORT] The port it: {PORT}")
            break
        except: 
            PORT += 1
            ADDR = (SERVER, PORT)
    print(PORT)
    root.title(f'IP: {SERVER}     Port: {PORT}')
    threading.Thread(target=new_client_handler, args=()).start()
    message('server', msg='SERVER STARTED')


def kill(): 
    global clients
    for o, i in enumerate(clients.copy()):
        message(i[1], 'kick')
        i[0].close()
        clients.pop(0)
    lst.delete(0, END)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        kill()
        server.close()
        sys.exit()

def size(*args):
    print(root.winfo_height())
    print(root.winfo_width())

root = Tk()
root.geometry("705x475")
root.configure(background='gray92')

frame1=ttk.Frame(root,width=150,height=600)
frame1.pack(side=LEFT, ipadx=10, ipady=10)
frame2=ttk.Frame(root,width=400)
frame2.pack(side=RIGHT, padx=10, pady=20)

textbox = Text(frame2, bg='white')
textbox.config(state=DISABLED)
textbox.pack(side=TOP)

button = Button(frame2, text="Send", command=get_text)
button.pack(ipadx=5, ipady=5, pady=5)

entry = Entry(frame2)
entry.pack(fill=X)

lst = Listbox(frame1, width=15, height=20)
lst.pack(side=TOP, ipadx=10, ipady=10, padx=10, pady=5)

kick = Button(frame1, text='Kick', command=kick_client)
kick.pack(side=TOP, ipadx=5, ipady=5, pady=10)

s = Button(frame2, text ='Open', command=start)
s.pack(side=RIGHT, ipadx=5, ipady=5, padx=3)
e = Button(frame2, text ='Disconnect All Clients', command=kill)
e.pack(side=RIGHT, ipadx=5, ipady=5, padx=3)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Return>", get_text) 
root.mainloop()
