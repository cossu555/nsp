import http.server  # Import the library for creating an HTTP server


# Define a custom handler class for processing HTTP requests
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Fixing log messages
    def log_message(self, format, *args):
        pass
        
    def do_POST(self):
        """
        Handle an HTTP POST request.
        """

        try:
            # Read the content length header to determine the size of the incoming message
            content_length = int(self.headers['Content-Length'])

            # Read the message from the request body (based on the content length)
            message = self.rfile.read(content_length).decode('utf-8')

            # Print the received message to the server console
            print("Server received the message: " + message)

            # Send a 200 OK response status after successful processing
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Respond back with a success message
            self.wfile.write(b"Message received successfully")

        except KeyError as e:
            # If 'Content-Length' is missing in the headers, send a 400 Bad Request error
            print(f"Error: Missing 'Content-Length' header: {e}")
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Error: Missing 'Content-Length' header")

        except (ValueError, UnicodeDecodeError) as e:
            # Handle errors in content length conversion or message decoding
            print(f"Error processing the POST request: {e}")
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Error processing the POST request")

        except Exception as e:
            # General exception handling for any other errors
            print(f"Unexpected error: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

    def do_GET(self):
        """
        Handle an HTTP GET request. (This method is defined but not actively used in this implementation.)
        """

        try:
            # Send a 200 OK response status
            self.send_response(200)

            # Add a 'Content-type' header to indicate that the response is in HTML format
            self.send_header('Content-type', 'text/html')

            # Signal that all headers have been sent
            self.end_headers()

            # Write a simple response message to the client
            self.wfile.write(b"GET response")

        except Exception as e:
            # General exception handling for any GET request errors
            print(f"Unexpected error in GET request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

