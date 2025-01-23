# Import needed libraries
import socket

# Function for the second client to attempt a connection to the server
def second_client_attempt(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send a message to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")

        # Receive a response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed.")


if __name__=="__main__":
    host = "127.0.0.1"
    port=443
    second_client_attempt(host,port)
