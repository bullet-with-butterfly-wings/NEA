import socket as soc
import pickle
import threading as thr
import time

server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
IP = "172.20.12.57"
PORT = 9090

server.bind((IP,PORT))
server.listen()


def handle(NAME, addr,client):
    contacts = pickle.dumps(list(clients.keys())[:-1]) #be careful about the last one
    client.send(contacts)
    greeting = pickle.dumps(("new_client",(NAME,addr)))
    for c in clients.values():
        if c != client:
            c.send(greeting)
    while True:#all msg> (type, receiver, source), if disc or request
        try:
            msg = pickle.loads(client.recv(1048)) #all formating at server
            if msg[0] == "END":
                client.close()
                del clients[(NAME,addr)]
            else:
                c = clients[msg[1]]
                c.send(pickle.dumps(msg))
            
        except:
            client.close()
            del clients[(NAME,addr)]

"""
def updater():
    while True:
        data = pickle.dumps(list(clients.values()))
        for c in clients.keys():
            c.send(data)
"""

clients = {}
threads = {}


while True:
    client, addr = server.accept()
    client.send("Hello".encode("utf-8"))
    try:
        NAME = client.recv(1024).decode("utf-8")
        clients[(NAME,addr)] = client
        print(f"{NAME} is here:",addr)
        threads[(NAME,addr)] = thr.Thread(target=handle, args=(NAME,addr,client))
        threads[(NAME,addr)].start()
    except:
        print("Bad Luck")