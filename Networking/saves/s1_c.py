import socket as soc
import threading as thr

client = soc.socket(soc.AF_INET,soc.SOCK_STREAM)
#server details
IP = "192.168.0.111"
PORT = 9090

name = input("Name:")
msg = ""

def server():
    try:
        info = client.recv(1024)
        print(info)
        if info == "YOUR NAME":
            client.send(name.encode("utf-8"))
        if info == "request":
            client.send()
    except:
        client.close()

def user():
    pass


client.connect((IP,PORT))
info = client.recv(1024)
client.send(name.encode("utf-8"))
print(info)
        
while msg != "END":
    msg = input()
    try:
        client.send(msg.encode("utf-8"))
    except:
        client.close()
        break