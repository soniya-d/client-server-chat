import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345)) 

    client_name = client_socket.recv(1024).decode() 
    print(client_name)

    while True:
        message = input("Enter message ('exit' to disconnect): ")

        client_socket.send(message.encode()) 
        if message.lower() == "exit":
            break

        response = client_socket.recv(1024).decode()  
        print(f"Received from server: {response}")

    client_socket.close()

if __name__ == '__main__':
    start_client()
