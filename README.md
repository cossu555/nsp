**Instructions to use the code:**

You have to download the scripts as you can find here (same directories and python files' names). Later, you have to launch "main_malicious.py" and "main_benevolent.py" (they shouldn't be ran in parallel). These mains exploit functions that are in python files' imported (first lines of the code). 


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

The attack consists to not allow the benevolent client to switch from http to https. We do this by starting the malicious client first and every 10 seconds it sends a connection request to the server on port 443. The attack works because the server has a weakness: it allows only one client at a time to connect to port 443. In this way when the benevolent client tries to access it fails.

