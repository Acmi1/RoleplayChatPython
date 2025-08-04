import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            print(message.decode())
        except:
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == "exit":
            client_socket.close()
            break
        elif message.lower() == "reconnect":
            # Здесь можно добавить логику переподключения
            print("Reconnecting...")
        else:
            client_socket.send(message.encode())

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    nickname = input("Enter your nickname: ")
    client_socket.send(nickname.encode())

    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    threading.Thread(target=send_messages, args=(client_socket,)).start()

if __name__ == "__main__":
    host = input("Enter server IP address: ")
    port = int(input("Enter server port: "))
    start_client(host, port)