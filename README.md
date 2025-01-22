**Instructions to use the code:**

You have to download the scripts as you can find here (same directories and python files' names). Then, it's necessary to put these commands on the terminal (order isn't important): "pip install cryptodome" and "pip install cryptography". Later, you have to run the file called "interface.py" which cosists of the interface of our program. After launching it you could choose which scenario, malicious or benevolent, you want to see (it could do this after importing and calling "main_malicious.py" or "main_benevolent.py").



About the execution of the code on Virtual Machines(VM) it's crucial to put the following commands on the terminal: "pip install cryptodome" and "pip install cryptography" before the running of the scripts.

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

This attack consists to not allow the benevolent client to switch from http to https. We do this by starting the malicious client first and every 10 seconds it sends a connection request to the server on port 443. The attack works because the server has a weakness: it allows only one client at a time to connect to port 443. In this way when the benevolent client tries to access it fails.

6._Implementation on Virtual Machines_:

At the end, we run our code on two different virtual machines which work one as the client and one as the server, in order to see the comunication and the packets' exchange. In this part, we separate the client from the server because we have two different addresses associated to two different machines, this implementation is different from the previous one where we use the local host's as address of both client and server.

**Requirements:**

-we suggest to use as IDE the PyCharm's version 3.12 or following because it could present exceptions in previous versions. 

-You couldn't run this code using Google Colab beacuse it doesn't allow executing code that uses port 80 or other directly accessible network ports for various reasons related to security and the service's architecture. 

-Problems could be presented also in other online IDEs (such as Replit or Gitpod) because some online IDEs (for example Replit) allow networking, but often redirect ports in a specific range, such as 3000-5000. Use of privileged ports (such as 80 and 443) is generally blocked. Complex networking functions such as TCP handshakes or key exchanges may fail due to limitations in connection configuration. So, it may not work unless you change the ports and check the environment texts.

-Environments with Network Restrictions (e.g. University or Corporate) because the environment may block specific ports, such as 80 and 443, or limit non-standard TCP connections for security reasons. So, it's possibile that it doesn't work due to network policies.

Possible solutions to make the code more portable in a specific IDE:

Change ports: Use unprivileged ports, such as 8080 (HTTP) and 8443 (HTTPS).

Control privileges: Run with elevated permissions only if necessary and in local environments.

Configure the environment: Check and configure firewalls, network rules, and available ports.
