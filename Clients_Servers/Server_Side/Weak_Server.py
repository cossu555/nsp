"""# Import needed libraries
import socket
from threading import Thread

# Function to start the server in a separate thread
def start_server(host, port):
    start_thread = Thread(target=_start_server, args=(host, port))
    start_thread.daemon = True
    start_thread.start()

# Function to initialize and run the server
def _start_server(host, port):
    # Create a TCP socket for the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the server socket to the specified host and port
        server_socket.bind((host, port))
        # Start listening for incoming connections, with a queue size of 1
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        # Continuously wait for and handle client connections
        while True:
            print("Waiting for a connection...")
            conn, addr = server_socket.accept()  # Accept an incoming connection
            with conn:
                print(f"Connected to {addr}")
                handle_client(conn)  # Handle communication with the client
                print(f"Connection closed with {addr}")

# Function to handle client communication
def handle_client(conn):
    while True:
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break  # Exit the loop if no data is received
        print(f"Received: {data.decode('utf-8')}")
        # Send a response back to the client
        conn.sendall(b"Received")
"""

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"server listening on {host}:{port}")

    client_socket,client_address = server_socket.accept()

    print(f"Connection Accepted from {client_address}")
    client_socket.close()
    server_socket.close()
