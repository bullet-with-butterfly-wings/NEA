from client import *


class Server(soc.socket):
    def __init__(self, family=soc.AF_INET, type=soc.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno)
        l = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        l.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = l.getsockname()[0]
        print("Server",local_ip_address)
        self.IP = local_ip_address #server details
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
                self.clients[addr] = client
                print(f"Server: {str(addr)} is here")
                self.threads[addr] = thr.Thread(target=self.handle, args=(addr,client))
                self.threads[addr].start()
            except:
                print("Server: Bad Luck")
    
    def handle(self, addr,client):
        contacts = pickle.dumps(list(self.clients.keys())[:-1]) #be careful about the last one
        client.send(contacts)        
        self.broadcast("new_client", addr[0] +" "+str(addr[1])) #must convert back
        while True:#all msg> (type, receiver, source), if disc or request
            try:
                msg = pickle.loads(client.recv(4096))
                #if len(msg) == 0:
                #    break
                print("Server:",msg.info())
                if msg.type == "END":
                    client.close()
                    del self.clients[addr]
                else:
                    if msg.receiver:
                        c = self.clients[msg.receiver]
                        c.send(pickle.dumps(msg))
            except:
                client.close()
                del self.clients[addr]
    
    def sending(self,type,receiver, text = None):
        if text:
            msg = Message(type,receiver,self.getsockname(), text)#Message(type,receiver,("SERVER",self.getsockname()),text)
        else:
            msg = Message(type,receiver,self.getsockname())#Message(type,receiver,("SERVER",self.getsockname()))
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