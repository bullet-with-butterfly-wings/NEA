import socket as soc
import threading as thr
import pickle



class Message: #does not work, new format [type, receiver, source, text]
    def __init__(self, type, receiver, source, text = None): #
        self.type = type
        self.receiver = receiver
        self.source = source
        self.text = text
    
    def info(self):
        print((self.type,self.receiver,self.source,self.text))

class Client(soc.socket):
    def __init__(self,family=soc.AF_INET, type=soc.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno)
        self.connected = False
        self.PORT = 9090
        f = open("IP.txt", "r")
        self.IP = f.read()
        f.close()
        self.buddy = None
        self.state = "connecting"
        self.text = None
        self.settimeout(2)
        self.connect((self.IP,self.PORT))
        self.settimeout(None)
        print(self.recv(1024).decode("utf-8"))#greeting from the server
        self.contacts = pickle.loads(self.recv(4096))
        print(self.contacts)
        self.up = thr.Thread(target= self.updater)
        self.up.start()
        self.protocols = ["",""]

    def send_msg(self, type, receiver, text = None):
        if type == "request":
            self.buddy = receiver
        if text:
            msg = Message(type,receiver,self.getsockname(), text)#Message(type,receiver,(self.Name,self.getsockname()),text)
        else:
            msg = Message(type,receiver,self.getsockname()) #Message(type,receiver,(self.Name,self.getsockname()))
        #picklefile_s = open('buffer', 'wb')
        #m = pickle.dump(msg,picklefile_s)
        #picklefile_s.close()
        msg.info()
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
                    if self.getsockname() != (new[0],int(new[1])):
                        self.contacts.append((new[0],int(new[1])))
                        print(self.contacts) #later sort out if list or str
                if action.type == "request":
                    self.state = "received_request"
                    self.buddy = action.source
                    self.protocols = action.text.split(" ")
                    print(f"Client {action.source} wants to chat with you")
                    #decision = "accept"#make actual decision
                    #self.connected = True
                if action.type == "response": #and self.buddy == action.source:
                        if action.text == "accept":
                            self.connected = True
                            self.state = "accepted"
                        else:
                            self.state = "rejected"
                            
            while self.connected:
                action = pickle.loads(self.recv(4096)) #Pickle object
                if action.type == "message" and action.source == self.buddy:
                    print(f"From {action.source}:",action.text)
                    self.state = "received"
                    self.text = action.text
                if action.type == "protocols":
                    self.text = action.text

    def response(self, decision):
        self.send_msg("response", self.buddy, decision)

    def initialiser(self, protocols, partner): 
        self.send_msg("request", self.contacts[partner], protocols[0]+" "+protocols[1])
        


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
    s = Client()