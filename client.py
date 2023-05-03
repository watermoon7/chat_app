import socket, threading, utils, sys, time, re
from tkinter import messagebox
from tkinter import *

# login
from login import *

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
