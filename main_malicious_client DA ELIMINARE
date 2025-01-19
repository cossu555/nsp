# Import needed libraries
import http.client
import time

def persistent_connection_to_server():

    # This client persistently tries to connect to the server's port 443 until it succeeds
    # Once it is connected, it send a request and receive a response
    while True:
        try:
            # Try to connect to server's port 443 (HTTPS)
            print("Connection's attempt to the sever on the 443 port...")
            conn = http.client.HTTPSConnection("127.0.0.1", 443, timeout=5)  # Modify the host if it's necessary
            conn.request("GET", "/")  # Send a simple GET request

            # Retrieve the response
            response = conn.getresponse()
            print(f"Successfully connected! Server's response: {response.status} - {response.reason}")
            print("Response's content:", response.read().decode())

            conn.close()
            break  # Get out from the cycle once the connection is established
        except Exception as e:
            print(f"Error during the connection: {e}. Retry in 1 second...")
            time.sleep(1)  # Wait a second before to retry

if __name__ == "__main__":
    persistent_connection_to_server()
