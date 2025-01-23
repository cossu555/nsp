import VirtualM.Benevolent.VM_server as VM_server

server = VM_server.VMServer()

port = int(input("Enter the port: "))
ip = input("Enter the IP: (suggestion: 0.0.0.0) ")

server.VM_start_conn(ip, port)

input("Press enter to continue:(1)")

server.VM_CHERTIFICATE_check()

input("Press enter to continue:(9)")

server.key_exchange()

input("Press enter to continue:(11)")

server.recieve_msg()