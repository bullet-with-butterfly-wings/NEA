from email import message
import socket as soc
import threading as thr

HEADER = 64
PORT = 5050
FORMAT = "utf-8" 
DISCONNECT_MESSAGE = "NO"

SERVER = "172.20.10.6"
SERVER = soc.gethostbyname(soc.gethostname()) #the same as line before
ADDR = (SERVER,PORT)
print(SERVER)

server = soc.socket(soc.AF_INET, soc.SOCK_STREAM) # make socket
server.bind(ADDR)

def client_handling(conn, addr):
  print(f"New client:{addr} \n") 
  connected = True
  while connected:
    msg_len = conn.recv(HEADER).decode(FORMAT) # first message is size of a next message
    if msg_len:
      msg_len = int(msg_len)
      msg = conn.recv(msg_len).decode(FORMAT)
      #here is the actual thing
      if msg == DISCONNECT_MESSAGE:
        connected = False
        print(thr.active_count()-2)
      else:
        print(msg)

  conn.close()


server.listen()
while True:
  conn, addr = server.accept() # stop and wait for client
  thread = thr.Thread(target = client_handling, args  = (conn, addr)) #make new thread
  thread.start()
  print(thr.active_count()-1)
