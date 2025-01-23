import VirtualM.Benevolent.VM_client as VM_client

client = VM_client.VMClient()

port = int(input("Enter port number: "))
ip = input("Enter ip: (suggestion: 172.20.10.13)")


#start HTTPS
client.VM_start(ip, port)
input("Press enter to continue:(0)")
client.VM_CERTIFICATE_Check()
input("Press enter to continue:(8)")
client.key_exchange()
input("Press enter to continue:(10)\n")
client.send_a_msg(input("Enter message for the server: "))

