import socket
import tkinter
from tkinter import *
from threading import Thread
import time

def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END,msg)
        except:
            print("There is an error receiving the message")
            break

window = Tk()
window.title("Chat Room Application")
window.config()

def send():
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))

    if msg == "/quit":
        s.close()
        window.quit()

def on_closing():
    my_msg.set("/quit")
    send()

message_frame = Frame(window, height=100, width=100)
message_frame.pack()

my_msg = StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, height=15, width=100, yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)

label = Label(window, text="Enter the message: ",font="Aeria")
label.pack()

entry_field = Entry(window, textvariable=my_msg, fg="red", width=50)
entry_field.pack()

send_button = Button(window, text="Send", font="Arial", fg="white", command=send)
send_button.pack()

quit_button = Button(window, text="Quit", font="Arial", fg="white", command=on_closing)
quit_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)


host = "localhost"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

receive_thread = Thread(target=receive)
receive_thread.start()


mainloop()