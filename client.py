import socket
import threading

name = input("What is your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 33333))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(name.encode("ascii"))
            elif "disconnect" in message:
                break
            elif "whisper" in message:
                if f"whisper {name}" in message:
                    print(f"Whisper received from {message.replace(f'whisper {name}', '')}")
            else:
                print(message)

        except:
            print("Disconnected from the server.")
            client.close()
            break


def write():
    while True:
        message = f'{name}: {input("")}'
        client.send(message.encode("ascii"))
        if "disconnect" in message:
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()