import socket
import threading
import csv
import os
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 4000

client_id = 0

# Function to handle each client connection
def handle_client_connection(client_socket, client_address, client_id):
    prev_x1_position = None
    prev_x2_position = None

    while True:
        # Check if the file exists
        if os.path.exists('output.csv'):
            # Process the CSV file received from the client
            with open('output.csv', 'r') as file:
                csv_reader = csv.reader(file)
                #next(csv_reader) # Skip header if present

                for row in csv_reader:
                    if len(row) == 3:
                        x1_position = float(row[0])
                        x2_position = float(row[1])

                        if x1_position is not None and x2_position is not None:
                            print(f"Received eye tracking data csv data from Client {client_id}: x1 position = {x1_position}, x2 position = {x2_position}")

                            if prev_x1_position is not None and prev_x2_position is not None:
                                x1_difference = x1_position - prev_x1_position
                                x2_difference = x2_position - prev_x2_position
                                print(f"Differences in positions: x1 = {x1_difference}, x2 = {x2_difference}")

                            prev_x1_position = x1_position
                            prev_x2_position = x2_position

                        else:
                            print("Invalid eye tracking data format.")
                    else:
                        print("Invalid CSV row format.")
            break  # Exit the loop once the file is processed

        # Sleep for a while before checking again
        time.sleep(1)

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
