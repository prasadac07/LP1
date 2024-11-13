import socket
import threading

def start_echo_server():
    host = '127.0.0.1'  # Localhost
    port = 12345        # Any available port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on",host,port,"")

    # Function to handle each client connection
    def handle_client(client_socket):
        message = client_socket.recv(1024).decode('utf-8')
        print("Received message:" ,message)
        client_socket.send(message.encode('utf-8'))
        client_socket.close()

    # Accept connections and start a new thread for each client
    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection established with ",client_address)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Start the server
start_echo_server()
