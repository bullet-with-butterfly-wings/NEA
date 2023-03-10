from client import *


class Server(soc.socket):
    def __init__(self, family=soc.AF_INET, type=soc.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno)
        self.IP = "192.168.0.200" #server details
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


if __name__ == "__main__":
    s = Server()
    s.listening()