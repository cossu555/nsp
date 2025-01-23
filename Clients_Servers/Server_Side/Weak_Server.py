import socket
import time
from threading import Thread

# Block duration in seconds
BLOCK_DURATION = 60  # For example, 60 seconds

def start_server(host, port):
    start_thread = Thread(target=_start_server, args=(host, port))
    start_thread.daemon = True  # Ensure the thread will not block program exit
    start_thread.start()

def _start_server(host, port):
    # Dictionary to track blocked IPs
    blocked_ips = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allows up to 5 queued connections
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        client_ip, client_port = client_address

        # Check if the IP is blocked
        current_time = time.time()
        if client_ip in blocked_ips:
            # Verify if the block duration has expired
            if current_time < blocked_ips[client_ip]:
                print(f"Connection denied for {client_ip}. IP is temporarily blocked.")
                client_socket.close()
                continue
            else:
                # Unblock the IP if the block duration has expired
                del blocked_ips[client_ip]

        # Connection accepted
        print(f"Connection accepted from {client_ip}:{client_port}")
        print("Server received:", client_socket.recv(1024))
        client_socket.close()

        # Block the IP for the specified duration
        blocked_ips[client_ip] = current_time + BLOCK_DURATION
        print(f"IP {client_ip} is now blocked for {BLOCK_DURATION} seconds.")
