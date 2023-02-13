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
from actual_gui import protocols
import signal
import time
import os
import sys

    
def gui_handler(signum, frame):
    print("Update:", window.state)
    if window.state == "intro":
        window.intro()
    elif window.state == "making_request":
        print(loco.contacts) 
        arg = []
        for c in loco.contacts:
            arg.append(c[0]+str(c[1])) 
            window.making_request(arg) 
    elif window.state == "waiting_for_response":
        loco.initialiser(protocols,window.partner)
    elif window.state == "response":
        pass
    elif window.state == "answered_request":
        loco.response(window.decision)
        if window.decision:
            window.chatroom()#protocols
        else:
            window.protocols = ("","")
            window.buddy = None
            window.intro()
    #print("Update:",loco.state)
    #if loco.state == "received_request":
    #    window.response(loco.buddy,loco.protocols)
    
def check():
    pre_g = ""
    while True:
        time.sleep(1)
        #print("Window:",window.state)
        #print("Client:",loco.state)
        if window.state != pre_g:
            os.kill(int(pid),signal.SIGUSR1)
            pre_g = window.state
            print("Check_win:", window.state)
        """
        if loco.state != pre_c:
            os.kill(int(pid),signal.SIGUSR1)
            pre_c = loco.state
            print("Check_cli:",loco.state)
        """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    global loco
    loco = Client()
    global window
    window = Scene()
    window.intro()        
    global pid
    pid = os.getpid()
    print(pid)    
    signal.signal(signal.SIGUSR1, gui_handler)
    #signal.signal(signal.SIGUSR2, client_handler)
    t = thr.Thread(target= check)
    t.start()
    sys.exit(app.exec_())