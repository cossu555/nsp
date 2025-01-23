# Import needed libraries
import socket

# Function for the second client to attempt a connection to the server
def second_client_attempt(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Benevolent_client: Try to connect to server at {host}:{port}")

        # Send a message to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode('utf-8'))
        print(f"B_Client: Sent: {message}")
        recieve=client_socket.recv(1024)
        print(f"B_Client: Received: {recieve}")
    except Exception as e:
        print(f"B_Client: Error: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print("B_Cient: Connection closed.")
