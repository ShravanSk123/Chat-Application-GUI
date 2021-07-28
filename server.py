import socket
import threading

HOST = 'localhost'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
usernames = []


# broadcast - send soething to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# handle - handle individual connections
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            break


# receive - listen and accept new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("USER".encode('utf-8'))
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print(f"Username is : {username}")
        broadcast(f"{username} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))  # , makes it a tuple
        thread.start()


print("Server running!!")
receive()
