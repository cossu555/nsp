1.HTTP Connection:

The client first establishes a connection with the server over HTTP on port 80 and sends a "Hi server" message.
The client then disconnects from the HTTP server.

2.HTTPS Protocol:

The connection switches to HTTPS, and a 3-way TCP handshake is performed between the client and server.
The client verifies the server's certificate to ensure it’s trusted.
A session key is securely exchanged between the client and server using RSA encryption.

3.Encrypted Messaging:

Once the session key is established, the client and server can securely exchange messages using AES encryption.

4.Message Transmission:

The client sends a message to the server, which is encrypted using the session key. The server decrypts the message to read it.

5.MitM attack

In addition to the benevolent client, the project includes a malicious client that simulates a Man-in-the-Middle (MitM) attack. It intercepts the messages between the benevolent client and the server, forwarding them while logging the data. This malicious client persistenly tries to access to 443 port until it succeeds, then it tries to convert an HTTPS connection in HTTP connection, it's an SSL stripping attack (a particular type of man in the middle attack). It aims to make more unsecure the connection in order to damage the comunication between server and client.

6.Attack's testing

The program uses threading to simulate the interaction between the benevolent client and the malicious client. The testing begins by creating threads for both clients, with the malicious client accessing to the port before the benevolent client, damaging in this way the connection.
