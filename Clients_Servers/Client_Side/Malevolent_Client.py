# Import needed libraries
import socket
import time
from threading import Thread

# Function to start a separate thread for connecting to the server
def connect_to_server(host, port):
    # Launch a background thread that repeatedly attempts to connect to the server
    start_thread = Thread(target=_connect_to_server, args=(host, port))
    start_thread.daemon = True  # Set the thread as daemon so it terminates with the main program
    start_thread.start()

# Internal function to repeatedly attempt connection to the server
def _connect_to_server(host, port):
    while True:
        try:
            # Try to establish a connection to the server at the specified host and port
            with socket.create_connection((host, port), timeout=5) as s:
                print(f"Malevolent Client: Successfully connected to {host} on port {port}.")
                break  # Exit the loop once the connection is successful
        except (socket.timeout, ConnectionRefusedError) as e:
            # If the connection fails, print the error and retry after a delay
            print(f"Malevolent Client: Connection failed: {e}. Retrying...")
            time.sleep(5)  # Wait 5 seconds before the next connection attempt
