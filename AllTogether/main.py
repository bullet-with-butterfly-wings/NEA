import sys
import time
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import asyncio
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from threading import Timer
from client import * 
import random
from actual_gui import protocols
import signal
import time
import os
import sys
from subprocess import call

    
def gui_handler():
    #if window.state == "intro":
    #    window.intro()
    if window.state == "making_request": 
        arg = []
        for c in loco.contacts:
            arg.append(c[0]+str(c[1])) 
        window.making_request(arg) 
    elif window.state == "waiting_for_response":
        loco.initialiser(protocols,window.partner)    
    elif window.state == "sending":
        loco.send_msg("message",loco.buddy, window.cipherText)
        window.state = "chatroom"
        loco.state = "in_call"
    
    elif window.state == "answered_request":
        if window.decision:
            loco.response("accept")
            loco.connected = True
            loco.send_msg("buffer",loco.getsockname(), "buffer")
            loco.state = "in_call"
            if loco.protocols == ["",""]:
                loco.protocols[0] = window.spojka()[0]
                loco.protocols[1] = window.spojka()[1]        
            else:
                window.solution(loco.protocols)
            if loco.protocols[0] == "RSA":
                call(["./generator"])    
                f = open("keys.out", "r")
                keys = f.readlines()
                loco.send_msg("protocols", loco.buddy, keys[0]+" "+keys[1])
                time.sleep(0.3)                
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
                time.sleep(0.2)
                B = int(loco.text)
                loco.symm_key = str(pow(B,a,n))
                window.symm_key = loco.symm_key
                print(loco.symm_key)
                window.dh(loco.protocols[1])
        else:
            loco.response("reject")
            window.protocols = ("","")
            window.buddy = None
            window.intro()
            loco.state = "connecting"

def cli_handler():
    if loco.state == "received_request":
        window.response(loco.buddy, loco.protocols)

    if loco.state == "accepted":
        window.waiting_for_response("Accepted")
        loco.state = "in_call"
        if loco.protocols == ["",""]:
            loco.protocols[0] = window.spojka()[0]
            loco.protocols[1] = window.spojka()[1]        
        else:
            window.solution(loco.protocols)
        if loco.protocols[0] == "RSA":
            time.sleep(0.2)
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
            time.sleep(0.2)
            B = int(loco.text)
            loco.symm_key = str(pow(B,a,n))
            print(loco.symm_key)
            #wait for message
            window.symm_key = loco.symm_key
            window.dh(loco.protocols[1])
        #initialize protocol    
                
    if loco.state == "rejected":
        window.waiting_for_response("Rejected")
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
        #time.sleep(2)
        f = open("buffer.txt", "r")
        plainText = f.read()
        f.close()
        window.sc.text_display.append(f"Buddy CipherText:{cipherText} \n     PlainText: {plainText}")
        loco.state = "in_call"

class Worker(QObject):
    finished = pyqtSignal()
    gui_change = pyqtSignal()
    cli_change = pyqtSignal()
    def check(self):
        pre_g = ""
        pre_c = ""
        while True:
            #print("Window:",window.state)
            #print("Client:",loco.state)
            if window.state != pre_g:
                self.gui_change.emit()
                pre_g = window.state
            if loco.state != pre_c:
                self.cli_change.emit()
                pre_c = loco.state
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    global loco
    loco = Client()
    global window
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