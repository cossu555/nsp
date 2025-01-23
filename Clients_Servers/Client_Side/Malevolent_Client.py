import socket
import time
from threading import Thread


# Starting a thread to attempt a connection to a server
def connect_to_server(host, port, num_attempts=70, delay=1):
    start_thread = Thread(target=_connect_to_server, args=(host, port, num_attempts, delay))
    start_thread.daemon = True      # Ensure the thread will not block program exit
    start_thread.start()


# Trying to connect to a server multiple times with a separate thread
def _connect_to_server(host, port, num_attempts, delay):
    for attempt in range(num_attempts):
        try:
            # Trying to establish a socket connection to the specified host and port
            with socket.create_connection((host, port), timeout=5) as s:
                print(f"Malevolent Client: Connection established to the server {host}:{port}")
                print(f"🚨 Warning: No data sent. Waiting for connection to close.")

                # Keeping the connection open without sending data for a short period
                time.sleep(delay * 2)

        # Handing connection timeout or refusal and retries after a delay
        except (socket.timeout, ConnectionRefusedError) as e:
            print(f"Attempt {attempt + 1}/{num_attempts} failed: {e}")
            time.sleep(delay)

        if attempt == num_attempts - 1:
            print("Connection attempts exhausted.")
