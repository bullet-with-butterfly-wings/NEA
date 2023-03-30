import sys
import time
import ctypes
import random
from subprocess import call
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QApplication


from client import * 
from gui import *
from server import *

def gui_handler():
    if window.state == "making_request": 
        arg = []
        for c in client.contacts:
            arg.append(c[0]+" "+str(c[1]))  
        window.making_request(arg)
    
    elif window.state == "waiting_for_response":
        client.initialiser(window.protocols,window.partner)    
    elif window.state == "sending":
        client.send_msg("message",client.buddy, window.cipherText)
        window.state = "chatroom"
        client.state = "in_call"
    elif window.state == "terminate":
        print("Bye!")
        #thread.exit()
        #ser.close()
        #client.close()

    elif window.state == "answered_request":
        print(window.decision)
        if window.decision:
            client.connected = True
            client.response("accept")
            client.send_msg("buffer", client.getsockname())
            client.state = "in_call"
            if client.protocols == ["",""]:
                client.protocols = window.protocols #maybe?
            else:
                window.protocols = client.protocols
                
            if client.protocols[0] == "RSA":
                call(["./ciphers/bin/generator"])    
                f = open("keys.out", "r")
                keys = f.readlines()
                client.send_msg("protocols", client.buddy, keys[0]+" "+keys[1])
                while not client.text:
                    time.sleep(0.1)
                client.symm_key = str(pow(int(client.text), int(keys[2]),int(keys[0]))) 
                window.symm_key = client.symm_key
                print(client.symm_key)
                window.rsa(client.protocols[1])#protocols
            else:
                #DH protocol
                n = 2147483647
                g = 7
                a = random.randint(1,n-1)
                A = pow(g,a,n)
                print(f"A:{A}, a:{a}")
                client.send_msg("protocols", client.buddy, str(A))
                while not client.text:
                    time.sleep(0.1)
                B = int(client.text)
                client.symm_key = str(pow(B,a,n))
                window.symm_key = client.symm_key
                print(client.symm_key)
                window.dh(client.protocols[1])
        else:
            window.protocols = ["",""]
            client.response("reject")
            window.buddy = None
            window.intro()
            client.state = "connecting"

def cli_handler():
    print(client.state)
    if client.state == "received_request":
        window.response(client.buddy, client.protocols)

    if client.state == "accepted":
        client.state = "in_call"
        if client.protocols == ["",""]:
            client.protocols = window.protocols  
        else:
            window.protocols = client.protocols
        
        if client.protocols[0] == "RSA":
            while not client.text:
                time.sleep(0.1)
            keys = client.text.split(" ")
            client.symm_key = str(random.randint(0,int(keys[0])-1))
            window.symm_key = client.symm_key
            print("Keys:", client.symm_key)
            client.send_msg("protocols", client.buddy, str(pow(int(client.symm_key), int(keys[1]), int(keys[0]))))
            window.rsa(client.protocols[1])
        else:
            #DH protocol
            n = 2147483647
            g = 7
            a = random.randint(1,n-1)
            A = pow(g,a,n)
            print(f"A:{A}, a:{a}")
            client.send_msg("protocols", client.buddy, str(A))
            while not client.text:
                time.sleep(0.1)
            B = int(client.text)
            client.symm_key = str(pow(B,a,n))
            print(client.symm_key)
            #wait for message
            window.symm_key = client.symm_key
            window.dh(client.protocols[1])
        #initialize protocol    
                
    if client.state == "rejected":
        client.state = "connecting"
        window.intro()
  
    if client.state == "received":
        cipherText = client.text
        f = open("buffer.txt", "w")
        f.write(cipherText)
        f.close()
        print("Should Decrypt")
        print(client.protocols[1])
        if client.protocols[1] == "Vernam":
            print("Decrypting")
            call(["./ciphers/bin/vernam", client.symm_key])
        else:
            call(["./ciphers/bin/feistel", "0", client.symm_key])
        #execute decrypting
        f = open("buffer.txt", "r")
        plainText = f.read()
        f.close()
        try: 
            window.sc.text_display.append(f"Buddy CipherText:{cipherText} \n      PlainText: {plainText}")
        except:
            print("Partner hasnot finished reading")
        client.state = "in_call"

class Worker(QObject):
    finished = pyqtSignal()
    gui_change = pyqtSignal()
    cli_change = pyqtSignal()
    
    def check(self):
        pre_g = ""
        pre_c = ""
        while True:
            if window.state != pre_g:
                self.gui_change.emit()
                pre_g = window.state
                
            if client.state != pre_c:
                    self.cli_change.emit()
                    pre_c = client.state
            
if __name__ == "__main__":
    myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    window = Scene()
    try:
        client = Client()
    except:
        s = Server()
        ser = thr.Thread(target=s.listening)
        ser.start()
        f = open("IP.txt","w")
        f.write(s.IP)
        f.close()
        client = Client()

    thread = QThread()
    # Step 3: Create a worker object
    worker = Worker()
        # Step 4: Move worker to the thread
    worker.moveToThread(thread)
        # Step 5: Connect signals and slots
    thread.started.connect(worker.check)
    worker.gui_change.connect(gui_handler)
    worker.cli_change.connect(cli_handler)

    # Step 6: Start the thread
    thread.start()
    sys.exit(app.exec_())