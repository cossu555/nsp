import http.server

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Read the message
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length).decode('utf-8')
        print("Server riceve il messaggio: " + message)

    #never used
    def do_GET(self):
        # Gestisci la richiesta GET
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Risposta GET")
