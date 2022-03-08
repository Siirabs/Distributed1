import threading
import socket

host ='127.0.0.1'
port = 33333

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []
channel1, channel2 = [], []



def broadcast_channel1(message):
    for client in channel1:
        client.send(message)
def broadcast_channel2(message):
    for client in channel2:
        client.send(message)
def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            decodedMessage = message.decode("ascii")
            index = clients.index(client)
            name = names[index]
            if "disconnect" in decodedMessage:
                clients.remove(client)
                client.close()
                print(f"User {name} disconnected.")
                broadcast(f"{name} left the channel".encode("ascii"))
                names.remove(name)
                break

            elif "channel1" in decodedMessage:
                if client not in channel1:
                    channel1.append(client)
                    if client in channel2:
                        channel2.remove(client)
                    print(f"Switched user {name} to channel 1.")
                    client.send("Switched to channel 1.".encode("ascii"))
                    continue
            elif "channel2" in decodedMessage:
                if client not in channel2:
                    channel2.append(client)
                    if client in channel1:
                        channel1.remove(client)
                    print(f"Switched user {name} to channel 2.")
                    client.send("Switched to channel 2.".encode("ascii"))
                    continue

            else:
                if client in channel1:
                    broadcast_channel1(message)
                elif client in channel2:
                    broadcast_channel2(message)
                else:
                    broadcast(message)
        except:
            clients.remove(client)
            if client in channel1:
                channel1.remove(client)
            if client in channel2:
                channel2.remove(client)
            client.close()
            broadcast(f"{name} left the channel".encode("ascii"))
            names.remove(name)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        name = client.recv(1024).decode("ascii")
        names.append(name)
        clients.append(client)

        print(f"Name of the client is {name}")
        broadcast(f"{name} joined the channel\n".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is runnning")
receive()