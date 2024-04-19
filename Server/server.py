import socket
import threading
import json

# Server configuration
HOST = '0.0.0.0'
PORT = 4000

client_id = 0

# Function to handle each client connection
def handle_client_connection(client_socket, client_address, client_id):
    # Initialize previous eye position
    prev_position = None

    # Receive data from client
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        try:
            # Parse received JSON data
            eye_data = json.loads(data)

            # Process recieved eye tracking data
            x_position = eye_data['x_position']
            if x_position is not None:
                print(f"Recieved eye tracking data from Client {client_id}: X position = {x_position}")

                # Calculate differene in positions
                if prev_position is not None:
                    difference = x_position - prev_position
                    print(f"Difference in positions: {difference}")

                # Update previous position
                prev_position = x_position
            else:
                print("Invalid eye tracking data format.")
        except json.JSONDecodeError:
            print("Error decoding JSON data.")
            continue    # Skip processing invalid JSON data

        # Process the received data
        #print(f"Received data from {client_socket.getpeername()}: {data.decode('utf-8')}")

    # Close the client socket when done 
    client_socket.close()

# Create a TCP/IP socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (allow up to 5 connections in the queue)
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")


while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Create a new thread to handle the connection
    client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address, client_id))
    client_thread.start()

    # Increment client_id for next client connection
    client_id += 1

    

    



