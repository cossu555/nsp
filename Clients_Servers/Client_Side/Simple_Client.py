# Import needed libraries
import socket
import ssl

# Function for the second client to attempt a connection to the server
def second_client_attempt(host, port):
    try:
        # Create a secure SSL context for the connection
        context = ssl.create_default_context()
        
        # Establish a TCP connection to the specified host and port
        with socket.create_connection((host, port)) as s:
            # Wrap the TCP connection in SSL for secure communication
            with context.wrap_socket(s, server_hostname=host) as ssl_sock:
                print("Benevolent Client: Second client connected to server.")
                
                # Send an HTTP GET request to the server
                request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                ssl_sock.sendall(request.encode())
                
                # Receive and print the server's response
                response = ssl_sock.recv(1024)
                print(f"Benevolent Client: Second client received: {response.decode()}")
    except Exception as e:
        # Handle and print any errors that occur during the connection
        print(f"Benevolent Client: Second client failed to connect: {e}")
