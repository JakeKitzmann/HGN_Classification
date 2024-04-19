import socket
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 3000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

# Accept incoming connections
client_socket, client_address = server_socket.accept()

print(f"Connection from {client_address}")

while True:
    # Receive data from client
    data = client_socket.recv(1024).decode()

    if not data:
        break

    # Parse received JSON data
    eye_data = json.loads(data)

    # Process recieved eye tracking data
    x_position = eye_data['x_position']
    print(f"Recieved eye tracking data: X position = {x_position}")


# Close connection
client_socket.close()
client_socket.close()