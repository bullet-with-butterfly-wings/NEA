import sys
import time
import random
from subprocess import call
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QApplication

from client import * 
from actual_gui import *
    
def gui_handler():
    if window.state == "making_request": 
        arg = []
        for c in loco.contacts:
            arg.append(c[0]+" "+str(c[1]))  
        window.making_request(arg)
    elif window.state == "waiting_for_response":
        loco.initialiser(window.protocols,window.partner)    
    elif window.state == "sending":
        loco.send_msg("message",loco.buddy, window.cipherText)
        window.state = "chatroom"
        loco.state = "in_call"
    elif window.state == "answered_request":
        print(window.decision)
        if window.decision:
            loco.connected = True
            loco.response("accept")
            loco.send_msg("buffer", loco.getsockname())
            loco.state = "in_call"
            if loco.protocols == ["",""]:
                loco.protocols = window.protocols #maybe?
            else:
                window.protocols = loco.protocols
                
            if loco.protocols[0] == "RSA":
                call(["./generator"])    
                f = open("keys.out", "r")
                keys = f.readlines()
                loco.send_msg("protocols", loco.buddy, keys[0]+" "+keys[1])
                while not loco.text:
                    time.sleep(0.1)
                loco.symm_key = str(pow(int(loco.text), int(keys[2]),int(keys[0]))) 
                window.symm_key = loco.symm_key
                print(loco.symm_key)
                window.rsa(loco.protocols[1])#protocols
            else:
                #DH protocol
                n = 2147483647
                g = 7
                a = random.randint(1,n-1)
                A = pow(g,a,n)
                print(f"A:{A}, a:{a}")
                loco.send_msg("protocols", loco.buddy, str(A))
                while not loco.text:
                    time.sleep(0.1)
                B = int(loco.text)
                loco.symm_key = str(pow(B,a,n))
                window.symm_key = loco.symm_key
                print(loco.symm_key)
                window.dh(loco.protocols[1])
        else:
            window.protocols = ["",""]
            loco.response("reject")
            window.buddy = None
            window.intro()
            loco.state = "connecting"

def cli_handler():
    print(loco.state)
    if loco.state == "received_request":
        window.response(loco.buddy, loco.protocols)

    if loco.state == "accepted":
        loco.state = "in_call"
        if loco.protocols == ["",""]:
            loco.protocols = window.protocols  
        else:
            window.protocols = loco.protocols
        
        if loco.protocols[0] == "RSA":
            while not loco.text:
                time.sleep(0.1)
            keys = loco.text.split(" ")
            loco.symm_key = str(random.randint(0,int(keys[0])-1))
            window.symm_key = loco.symm_key
            print(loco.symm_key)
            loco.send_msg("protocols", loco.buddy, str(pow(int(loco.symm_key), int(keys[1]), int(keys[0]))))
            window.rsa(loco.protocols[1])
        else:
            #DH protocol
            n = 2147483647
            g = 7
            a = random.randint(1,n-1)
            A = pow(g,a,n)
            print(f"A:{A}, a:{a}")
            loco.send_msg("protocols", loco.buddy, str(A))
            while not loco.text:
                time.sleep(0.1)
            B = int(loco.text)
            loco.symm_key = str(pow(B,a,n))
            print(loco.symm_key)
            #wait for message
            window.symm_key = loco.symm_key
            window.dh(loco.protocols[1])
        #initialize protocol    
                
    if loco.state == "rejected":
        loco.state = "connecting"
        window.intro()
  
    if loco.state == "received":
        cipherText = loco.text
        f = open("buffer.txt", "w")
        f.write(cipherText)
        f.close()
        print("Should Decrypt")
        print(loco.protocols[1])
        if loco.protocols[1] == "Vernam":
            print("Decrypting")
            call(["./vernam", loco.symm_key])
        else:
            call(["./feistel", "0", loco.symm_key])
        #execute decrypting
        f = open("buffer.txt", "r")
        plainText = f.read()
        f.close()
        try: 
            window.sc.text_display.append(f"Buddy CipherText:{cipherText} \n      PlainText: {plainText}")
        except:
            print("Partner hasnot finished reading")
        loco.state = "in_call"

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
            if loco.state != pre_c:
                self.cli_change.emit()
                pre_c = loco.state
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loco = Client()
    window = Scene()

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