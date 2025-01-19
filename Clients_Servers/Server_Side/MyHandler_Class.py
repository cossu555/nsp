import http.server  # Import the library for creating an HTTP server

# Define a custom handler class for processing HTTP requests
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        
        """
        Handle an HTTP POST request.
        """
        
        # Read the content length header to determine the size of the incoming message
        content_length = int(self.headers['Content-Length'])

        # Read the message from the request body (based on the content length)
        message = self.rfile.read(content_length).decode('utf-8')

        # Print the received message to the server console
        print("Server received the message: " + message)

    def do_GET(self):
        
        """
        Handle an HTTP GET request. (This method is defined but not actively used in this implementation.)
        """
        
        # Send a 200 OK response status
        self.send_response(200)

        # Add a 'Content-type' header to indicate that the response is in HTML format
        self.send_header('Content-type', 'text/html')

        # Signal that all headers have been sent
        self.end_headers()

        # Write a simple response message to the client
        self.wfile.write(b"GET response")
