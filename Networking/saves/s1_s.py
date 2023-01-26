import socket as soc
import threading as thr

server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
IP = "192.168.0.111"
PORT = 9090

server.bind((IP,PORT))
server.listen()


def handle(client):
    while True:
        try:
            msg = client.recv(1048)
            print(msg.decode("utf-8"))
        except:
            client.close()
            del clients[client]



clients = {}
while True:
    client, addr = server.accept()
    client.send("Hello".encode("utf-8"))
    print("Hi")
    try:
        NAME = client.recv(1024).decode("utf-8")
        clients[client] = NAME
        print(NAME)
        thread = thr.Thread(target=handle, args=(client,))
        thread.start()
    except:
        print("Bad Luck")