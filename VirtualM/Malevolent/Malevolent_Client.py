# Import needed libraries
import socket
import time
from threading import Thread

# Internal function to repeatedly attempt connection to the server, this time there is no thread
def connect_to_server(host, port):
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

if __name__ == "__main__":
    connect_to_server(input("insert IP to attack: (suggestion: 172.20.10.13) "), 8080)