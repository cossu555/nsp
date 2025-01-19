1.HTTP Connection:

The client first establishes a connection with the server over HTTP on port 80 and sends a "Hi server" message.
The client then disconnects from the HTTP server.

2.HTTPS Protocol:

The connection switches to HTTPS, and a 3-way TCP handshake is performed between the client and server.
The client verifies the server's certificate to ensure it’s trusted.
A session key is securely exchanged between the client and server using RSA encryption.

3.Encrypted Messaging:

Once the session key is established, the client and server can securely exchange messages using AES encryption.
Message Transmission:The client sends a message to the server, which is encrypted using the session key. The server decrypts the message to read it.

4.MitM attack

