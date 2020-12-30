import socket
from threading import Thread

host = "localhost"
port = 8080
clients = {}
addresses = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

def handle_clients(conn, address):
    name = conn.recv(1024).decode()
    welcome = "Welcome "+name+ " ! You can type /quit if you ever want to leave the Chat Room"
    conn.send(bytes(welcome, "utf8"))
    msg = name + " has recently joined the room"
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name

    while True:
        msg = conn.recv(1024)
        if msg != bytes("/quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            print("Quitter")
            conn.send(bytes("/quit","utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(name + " has left the Chat Room !", "utf8"))
            break

def accept_client_conn():
    while True:
        client_conn, client_address = sock.accept()
        print(client_address, "has connected")
        client_conn.send("Welcome to the chat room, please type your name:".encode('utf8'))
        addresses[client_conn] = client_address
        Thread(target=handle_clients, args=(client_conn, client_address)).start()

def broadcast(msg, prefix=""):
    for x in clients:
        x.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    sock.listen(5)
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    t1 = Thread(target=accept_client_conn)
    t1.start()
    t1.join()
    sock.close()
