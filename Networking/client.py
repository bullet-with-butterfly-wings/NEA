import socket as soc
import threading as thr
import pickle
import time


client = soc.socket(soc.AF_INET,soc.SOCK_STREAM)
#server details
IP = "172.20.12.57"
PORT = 9090

name = input("Name:")
msg = ("","")

client.connect((IP,PORT))
print(client.recv(1024).decode("utf-8"))
client.send(name.encode("utf-8"))
contacts = pickle.loads(client.recv(4096))
print(contacts)
receiver = -1
global connected
connected = False
#preparation done

class Message:
    def __init__(self, type, receiver, source, text = None): #
        self.type = type
        self.receiver = receiver
        self.source = source
        self.text = text
    def send(self):
        if text:
            msg = pickle.dumps((self.type,self.receiver,self.source, self.text))
        else:
            msg = pickle.dumps((self.type,self.receiver,self.source, self.text))
        client.send(msg)

def updater():
    while True:
        global connected
        while not connected:
            action = pickle.loads(client.recv(4096))
            #now depends
            if action[0] == "new_client":
                contacts.append(action[1])
                print(contacts)
            if action[0] == "request":
                print(f"Client {action[2][0]} wants to chat with you")
                decision = "accept"
                res = pickle.dumps(("response", contacts[receiver], (name,client.getsockname()), decision))
                client.send(res)
                connected = True
            if action[0] == "response" and contacts.index(action[2]) == receiver:
                    print(action[3])
                    if action[3] == "accept":
                        connected == True
        print("ehf")
        while connected:
            action = pickle.loads(client.recv(4096))
            if action[0] == "message":
                print(f"From {action[2][0]}:",action[3])
                msg_from = action[3]

up = thr.Thread(target=updater)
up.start()

while not connected: #you can request multiple people
    receiver = int(input("Choose partner (number):"))
    assymetric = input("Choose assymetric protocol (RSA or DH):")
    symmetric = input("Choose symmetric (Vernam or Feistel):")
    msg = pickle.dumps(("request", contacts[receiver], (name,client.getsockname()), assymetric+" "+symmetric))
    client.send(msg)
    print("Waiting...")
    time.sleep(10_000)

print("Message phase")

while connected:
    text = input()
    msg = pickle.dumps(("message", contacts[int(msg[1])], (name,client.getsockname()), text))
    try:
        client.send(msg) #for request put everything
    except:
        client.close()
        break