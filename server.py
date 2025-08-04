import socket
import threading

clients = {}

def handle_client(client_socket, addr):
    nickname = client_socket.recv(1024).decode()
    clients[nickname] = client_socket
    broadcast(f"{nickname} joined the chat!".encode())

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, nickname)
        except:
            break

    del clients[nickname]
    broadcast(f"{nickname} left the chat!".encode())
    client_socket.close()

def broadcast(message, sender=None):
    for nickname, client_socket in clients.items():
        if sender and nickname != sender:
            client_socket.send(message)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    host = input("Enter server IP address: ")
    port = int(input("Enter server port: "))
    start_server(host, port)