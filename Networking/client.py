import socket as soc
import threading as thr
import pickle

client = soc.socket(soc.AF_INET,soc.SOCK_STREAM)
#server details
IP = "192.168.0.111"
PORT = 9090

name = input("Name:")
msg = ""


client.connect((IP,PORT))
print(client.recv(1024).decode("utf-8"))
client.send(name.encode("utf-8"))
contacts = pickle.loads(client.recv(4096))
print(contacts)
#preparation done

def updater():
    while True:
        action = pickle.loads(client.recv(4096))
        #now depends
        if action[0] == "new_client":
            contacts.append(action[1])
            print(contacts)
        if action[0] == "request":
            print(f"Client {action[2][0]} wants to chat with you")
        if action[0] == "message":
            print(f"From {action[2][0]}:",action[3])
up = thr.Thread(target=updater)
up.start()

while msg[0] != "END":
    print("what do u want to do?")
    msg = input().split(" ")
    if msg[0] == "request": #message something
        msg = pickle.dumps(("request",contacts[int(msg[1])],(name,client.getsockname())))
    if msg[0] == "message":
        msg = pickle.dumps(("message", contacts[int(msg[1])], (name,client.getsockname()), " ".join(msg[2:])))
    
    #msg = pickle.dumps(("message",,client))
    try:
        client.send(msg) #for request put everything
    except:
        client.close()
        break