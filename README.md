**Instructions to use the code:**

You have to download the scripts as you can find here (same directories and python files' names) and then you have to launch "main_malicious.py" and "main_benevolent.py" (the order isn't important but they can't be ran in parallel). These mains exploit functions that are in python files' imported (first lines of the code). 


**Explanation of the code:**

1._HTTP Connection_:

The client first establishes a connection with the server over HTTP on port 80 and sends a "Hi server" message.

2._HTTPS Protocol_:

The server answers with a 301 redirect that resends the user to the HTTPS version of the site, so the connection switches to HTTPS, and a 3-way TCP handshake is performed between the client and server. The client verifies the server's certificate to ensure it’s trusted. A session key is securely exchanged between the client and server using RSA encryption.

3._Encrypted Messaging_:

Once the session key is established, the client and server can securely exchange messages using AES encryption.

4._Message Transmission_:

The client sends a message to the server, which is encrypted using the session key. The server decrypts the message to read it.

5._DoS attack_:

In addition to the benevolent client, the project includes a malicious client that simulates a Man-in-the-Middle (MitM) attack. This malicious client persistenly tries to access to 443 port until it succeeds, then it tries to convert an HTTPS connection in HTTP connection, it's an SSL stripping attack (a particular type of man in the middle attack). It aims to make more unsecure the connection in order to damage the communication between server and client.

