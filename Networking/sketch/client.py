from email.header import Header
import socket as soc

HEADER = 64
PORT = 5050
SERVER = "192.168.0.111"

FORMAT = "utf-8" 
DISCONNECT_MESSAGE = "NO" 
ADDR = (SERVER,PORT)

client = soc.socket(soc.AF_INET,soc.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length)) #fill the space
    client.send(send_length)
    client.send(message)

msg = ""
while msg != "NO":
    msg = input("Message:")
    send(msg)

send(DISCONNECT_MESSAGE)