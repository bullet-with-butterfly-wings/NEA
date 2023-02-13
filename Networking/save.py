from client import *


class Server(soc.socket):
    def __init__(self, family=soc.AF_INET, type=soc.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno)
        self.IP = "192.168.0.202" #server details
        self.PORT = 9090
        self.bind((self.IP,self.PORT))
        self.listen()      
        self.clients = {} #tady m83 i kontakty
        self.threads = {}
    def listening(self): #nepl0st si s listen (socket)
        while True:
            client, addr = self.accept()
            client.send("Hello".encode("utf-8"))
            try:
                NAME = client.recv(1024).decode("utf-8")
                self.clients[(NAME,addr)] = client
                print(f"{NAME} is here:",addr)
                self.threads[(NAME,addr)] = thr.Thread(target=self.handle, args=(NAME,addr,client))
                self.threads[(NAME,addr)].start()
            except:
                print("Bad Luck")
    
    def handle(self, NAME, addr,client):
        contacts = pickle.dumps(list(self.clients.keys())[:-1]) #be careful about the last one
        client.send(contacts)        
        self.broadcast("new_client",NAME+" "+ addr[0] +" "+str(addr[1])) #must convert back
        while True:#all msg> (type, receiver, source), if disc or request
            try:
                msg = pickle.loads(client.recv(4096))
                print(msg.info())
                if msg.type == "END":
                    client.close()
                    del self.clients[(NAME,addr)]
                else:
                    if msg.receiver:
                        c = self.clients[msg.receiver]
                        c.send(pickle.dumps(msg))
            except:
                client.close()
                del self.clients[(NAME,addr)]
    
    def sending(self,type,receiver, text = None):
        if text:
            msg = Message(type,receiver,("SERVER",self.getsockname()), text)#Message(type,receiver,("SERVER",self.getsockname()),text)
        else:
            msg = Message(type,receiver,("SERVER",self.getsockname()))#Message(type,receiver,("SERVER",self.getsockname()))
        #picklefile = open('buffer', 'wb')
        m = pickle.dumps(msg)
        self.clients[receiver].send(m)
        #picklefile.close()

    def broadcast(self, type, text=None):
        if text:
            for c in list(self.clients.keys()):
                self.sending(type, c, text)
        else:
            for i in list(self.clients.keys()):
                self.sending(type, c)

import socket as soc
import threading as thr
import pickle
import time


class Message: #does not work, new format [type, receiver, source, text]
    def __init__(self, type, receiver, source, text = None): #
        self.type = type
        self.receiver = receiver
        self.source = source
        self.text = text
        
    def info(self):
        print((self.type,self.receiver,self.source,self.text))

class Client(soc.socket):
    def __init__(self, family=soc.AF_INET, type=soc.SOCK_STREAM, proto=0, fileno=None, name=None):
        super().__init__(family, type, proto, fileno)
        self.Name = name
        self.connected = False
        self.IP = "192.168.0.202" #server details
        self.PORT = 9090
        self.buddy = None
        self.connect((self.IP,self.PORT))
        print(self.recv(1024).decode("utf-8"))#greeting from the server
        self.send(self.Name.encode("utf-8"))
        self.contacts = pickle.loads(self.recv(4096))
        print(self.contacts)
        self.up = thr.Thread(target= self.updater)
        self.up.start()
        self.protocols = ["Ass","Sym"]
        self.initialiser()
        self.running()
    
    def send_msg(self, type, receiver, text = None):
        if type == "request":
            self.buddy = receiver
        if text:
            msg = Message(type,receiver,(self.Name,self.getsockname()), text)#Message(type,receiver,(self.Name,self.getsockname()),text)
        else:
            msg = Message(type,receiver,(self.Name,self.getsockname())) #Message(type,receiver,(self.Name,self.getsockname()))
        #picklefile_s = open('buffer', 'wb')
        #m = pickle.dump(msg,picklefile_s)
        #picklefile_s.close()
        print(msg.info())
        m = pickle.dumps(msg)
        self.send(m)
        
    def updater(self):
        while True:
            while not self.connected:
                data = self.recv(4096)
                
                #picklefile_u = open('buffer', 'rb')
                #unpickle the dataframe
                #action = pickle.dumps(picklefile_u)
                #picklefile_u.close()
                
                action = pickle.loads(data)
                #close file
                #now depends
                if action.type == "new_client":
                    new = action.text.split()#nechto crashnout            
                    self.contacts.append((new[0],(new[1],int(new[2]))))
                    print(self.contacts) #later sort out if list or str
                if action.type == "request":
                    print(f"Client {action.source[0]} wants to chat with you")
                    decision = "accept"#make actual decision
                    #self.send_msg(Message("response", self.contacts[self.clients.index(action.source)], (self.Name,self.getsockname()), decision))
                    self.send_msg("response", action.source, decision)
                    self.connected = True

                if action.type == "response" and self.buddy == action.source:
                        print(action.text)
                        if action.text == "accept":
                            self.connected = True
            print("Connected with your buddy")
            while self.connected:
                action = pickle.loads(self.recv(4096)) #Pickle object
                if action.type == "message":
                    print(f"From {action.source[0]}:",action[3])
    
    def initialiser(self):
        while not self.connected: 
            r = int(input("Choose partner (number):"))
            self.protocols[0] = input("Choose assymetric protocol (RSA or DH):")
            self.protocols[1] = input("Choose symmetric (Vernam or Feistel):")#this will be substitued with actual gui
            self.send_msg("request", self.contacts[r], self.protocols[0]+" "+self.protocols[1])
            print("Waiting...") #Na class message (maybe) + sekne se na init()
            time.sleep(10)



    def running(self):
        while self.connected:
            text = input()
            try:
                self.send_msg("message",self.buddy,text)
            except:        
                self.close()
                self.connect = False
                break


if __name__ == "__main__":
    Name = input()
    loco = Client(name=Name)

if __name__ == "__main__":
    s = Server()
    s.listening()