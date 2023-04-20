import socket, threading, utils, commands

HEADER = 64
PORT = 5053
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
var = True
while var:
    try:
        server.bind(ADDR)
        print(f"[PORT] The port it: {PORT}")
        var = False
    except:
        PORT += 1
        ADDR = (SERVER, PORT)

msg_list = []
clients = []
def update():
    for c in clients:
        utils.send(c, ''.join(msg_list))


def handle_client(connection, addr, name):
    global msg_list
    print(f"[NEW CONNECTION] {name} at {addr} connected.")

    connected = True
    while connected:
        msg = utils.recieve(connection)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            msg_list.append(f'--- @ {name} has left the chat ---\n')
            print(f'--- @ {name} has left the chat ---')
        else:
            if msg in commands.commands:
                result = commands.commands[msg]()
                msg_list.append(f" {name} > {msg}\n")
                print(f" {name} > {msg}")
                msg_list.append(f"{result}\n")
                print(f"{result}\n")
            else:    
                msg_list.append(f" {name} > {msg}\n")
                print(f" {name} > {msg}")
        update()

    connection.close()
    clients.remove(connection)
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
        

def start():
    global msg_list
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:
        connection, addr = server.accept()
        clients.append(connection)
        
        name = utils.recieve(connection).strip()
        
        thread = threading.Thread(target=handle_client, args=(connection, addr, name))
        thread.start()
        
        msg_list.append(f'--- @ {name} has connected to the chat ---\n')
        update()
        print(f'--- @ {name} has connected to the chat ---')
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
