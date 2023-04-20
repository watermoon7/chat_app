import socket

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
