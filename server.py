import socket
import threading
from datetime import datetime

MAX_CLIENTS = 3 
clients = {}  

lock = threading.Lock()  
client_id = 1  


def handle_client(client_socket, client_address, assigned_id):
    client_name = f"Client{assigned_id:02d}"  
    connect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with lock:
        clients[client_name] = {"connect_time": connect_time, "disconnect_time": None}

    client_socket.send(f"Your assigned name: {client_name}".encode())

    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break  

            print(f"{client_name} sent: {data}")  

            if data.lower() == "exit":
                break  

            elif data.lower() == "status":
                status_message = "\n".join(
                    [f"{name}: Connected at {info['connect_time']}, Disconnected at {info['disconnect_time'] or 'Active'}"
                     for name, info in clients.items()])
                client_socket.send(status_message.encode())

            else:
                client_socket.send(f"{data} ACK".encode()) 

        except ConnectionResetError:
            break  

    disconnect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with lock:
        if client_name in clients:
            clients[client_name]["disconnect_time"] = disconnect_time
            del clients[client_name]  

    client_socket.close()
    print(f"{client_name} disconnected.")


def start_server():
    global client_id  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(MAX_CLIENTS)
    print("Server is listening...")

    while True:
        if len(clients) < MAX_CLIENTS:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            with lock:
                assigned_id = client_id  
                client_id += 1 

            threading.Thread(target=handle_client, args=(client_socket, client_address, assigned_id)).start()


if __name__ == '__main__':
    start_server()
