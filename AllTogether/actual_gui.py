
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

partne = -1
protocols = ["",""]
#contacts = ["John", "James", "Jane", "Jonas"]


class Scene(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 1000, 700)
        self.state = "intro"
        self.partner = -1
        self.decision = None
        self.setWindowTitle("Encryption Engine")
        
    def intro(self):
        self.sc = Intro()
        self.state = "intro"
        self.setCentralWidget(self.sc)
        #buttons 
        self.sc.continue_button.clicked.connect(lambda x, arg = "making_request":self.dummy(arg))
        self.show()
    def dummy(self, state):
        self.state = state

    def chatroom(self):
        self.state = "chatroom"
        print("COol")
        self.sc = Chatroom()
        self.setCentralWidget(self.sc)

    def making_request(self, contacts):
        print("Making request")
        self.state = "making_request"
        self.sc = RequestMaker(contacts)
        self.setCentralWidget(self.sc)
        pro_buttons = [self.sc.feistel_button, self.sc.rsa_button, self.sc.dh_button,  self.sc.vernam_button]
        titles = ["Feistel", "RSA", "DH", "Vernam"]
        
        for i in range(len(pro_buttons)):
            pro_buttons[i].clicked.connect(lambda idk, arg = (i, pro_buttons[i], pro_buttons[len(titles)-1-i]): self.protocols(titles[arg[0]], arg[1],arg[2]))
            pro_buttons[i].setCheckable(True)
        
        self.sc.send_button.setEnabled(False)
        self.sc.send_button.clicked.connect(lambda: self.waiting_for_response("Answer"))#send request
        self.sc.cancel_button.clicked.connect(self.intro)
        self.show()
        #contacts
        
        for i in range(len(contact_buttons)):
            contact_buttons[i].setCheckable(True)
            contact_buttons[i].clicked.connect(lambda idk, arg = i: self.contacts(arg))

    #these two functions governs contacts and protocols buttons    
    def contacts(self,pressed):
        self.partner = -1
        if not contact_buttons[pressed].isChecked():
            contacts_ready = False
        else:
            for i in range(len(contact_buttons)):
                if i == pressed:
                    contact_buttons[i].setChecked(True)
                    contacts_ready = True
                    self.partner = i
                    print(self.partner)
                else:
                    contact_buttons[i].setChecked(False)
                    
        if (protocols[0] != "" and protocols[1] != "") and contacts_ready:
            self.sc.send_button.setEnabled(True)
        else:
            self.sc.send_button.setEnabled(False)
        
    def protocols(self, pro, button, uncheck_button):
        i = int(pro in ["Vernam", "Feistel"])
        if not button.isChecked():
            protocols[i] = ""
        else: 
            protocols[i] = pro
            uncheck_button.setChecked(False)
        
        c_ready = False
        for c in contact_buttons:
            if c.isChecked():
                c_ready = True 

        if (protocols[0] != "" and protocols[1] != "") and c_ready:
            self.sc.send_button.setEnabled(True)
        else:
            self.sc.send_button.setEnabled(False)
        
        

    def response(self, partner, protocols):
        self.state = "recieved_request"
        self.sc = RequestReciever("("+partner[0]+str(partner[1])+")", " ".join(protocols))
        self.setCentralWidget(self.sc)
        self.sc.accept_button.clicked.connect(lambda: self.ans(True))
        self.sc.reject_button.clicked.connect(lambda: self.ans(False))
        self.show()
    
    def ans(self, decision):
        self.decision = decision
        self.state = "answered_request"

    def waiting_for_response(self, text):
        self.state = "waiting_for_response"
        self.sc = Waiting()
        self.setCentralWidget(self.sc)
        self.sc.decision.setText(text)
        self.show()
        


class Intro(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        intro_text = QLabel("""Welcome to the Encryption Engine, 
        a tool developed specifically for students to learn 
        about ciphers and their applications. 
        You have two possibilities now:
        """)
        wait_text = QLabel("or you can wait for someones request...")
        self.continue_button = QPushButton("Connect",self)

        layout.addWidget(intro_text)
        layout.addWidget(self.continue_button)
        layout.addWidget(wait_text)
        
        components = [self.continue_button,intro_text,wait_text]
        
        for c in components[1:]:
            c.setAlignment(Qt.AlignCenter)
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.continue_button.setStyleSheet("")

        layout.setContentsMargins(200, 100, 200, 100)
        self.continue_button.setFont(QFont("Ariel", 20))
        self.setLayout(layout)

class RequestMaker(QWidget):
    def __init__(self, contacts) -> None:
        super().__init__()
        label = QLabel("Select protocols:")
        label.setAlignment(Qt.AlignCenter)

        # Create pro_buttons
        self.rsa_button = QPushButton("RSA")
        self.rsa_button.setMinimumSize(QSize(80, 40))
        self.dh_button = QPushButton("Diffie-Hellman")
        self.dh_button.setMinimumSize(QSize(80, 40))
        self.vernam_button = QPushButton("Vernam")
        self.vernam_button.setMinimumSize(QSize(80, 40))
        self.feistel_button = QPushButton("Feistel")
        self.feistel_button.setMinimumSize(QSize(80, 40))

        self.send_button = QPushButton("Send")
        self.send_button.setMinimumSize(QSize(80, 40))
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumSize(QSize(80, 40))

        #self.rsa_button.clicked.connect(self.)
        #self.dh_button.clicked.connect(self.self.dh_button)

        # Create a grid layout and add pro_buttons and label
        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(QLabel("Assymetric encryption...", self), 1, 0, 1, 2)
        layout.addWidget(self.rsa_button, 2, 0)
        layout.addWidget(self.dh_button, 2, 1)
        layout.addWidget(QLabel("Symetric encryption...", self), 3, 0, 1, 2)
        layout.addWidget(self.vernam_button, 4, 0)
        layout.addWidget(self.feistel_button, 4, 1)
        layout.addItem(QSpacerItem(0, 20), 5, 0, 1, 2)
        layout.addWidget(self.send_button, 6, 1)
        layout.addWidget(self.cancel_button, 6, 0)

        # Create a separate vertical layout for contacts pro_buttons
        contacts_layout = QVBoxLayout()
        global contact_buttons 
        contact_buttons = []
        for c in contacts:
            contact_buttons.append(QPushButton(c))
            contact_buttons[-1].setMinimumSize(QSize(80, 40))
            contacts_layout.addWidget(contact_buttons[-1])
        
        contacts_layout.setContentsMargins(0, 0, 0, 0)


        layout.addLayout(contacts_layout, 0, 2, 7, 1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)
    
        layout.setContentsMargins(20, 50, 10, 50)
        self.setLayout(layout)


class Waiting(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Waiting for the decision")
        label.setAlignment(Qt.AlignCenter)            
        self.decision = QLabel("Answer??")
        self.decision.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(self.decision)
        layout.setContentsMargins(200, 100, 200, 100)
        self.setLayout(layout)


class RequestReciever(QWidget):
    def __init__(self, source, protocols) -> None:
        super().__init__()
        # Create a label to display the request message
        self.request_label = QLabel("You have received a request from " + source + " for the following protocols: " + protocols)
        self.request_label.setAlignment(Qt.AlignCenter)
        self.request_label.setMargin(20)

        # Create the accept button
        self.accept_button = QPushButton("Accept")
        self.accept_button.setStyleSheet("background-color: green")

        # Create the reject button
        self.reject_button = QPushButton("Reject")
        self.reject_button.setStyleSheet("background-color: red")
        
        self.reject_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.accept_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.request_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Create a horizontal layout to hold the pro_buttons
        pro_buttons_layout = QHBoxLayout()
        pro_buttons_layout.addWidget(self.accept_button)
        pro_buttons_layout.addWidget(self.reject_button)
        pro_buttons_layout.setContentsMargins(20, 0, 20, 20)

        # Create a widget to hold the layout
        pro_buttons_widget = QWidget()
        pro_buttons_widget.setLayout(pro_buttons_layout)

        # Set the layout of the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.request_label)
        main_layout.addWidget(pro_buttons_widget)
        main_layout.setContentsMargins(200, 100, 200, 100)

        self.setLayout(main_layout)

class IntroBack(QObject): #backgrounds
    def __init__(self):
        super().__init__()
        self.on = True
    finished = pyqtSignal()
    message = pyqtSignal(bool)
        
    def run(self):
        t = Timer(3.0,self.p)
        t.start()
        #input() here is a plan: when will timer finish, we will send a message to server to send us a message to make us free. For now, just ignore it
        time.sleep(5)
        if self.on:
            self.finished.emit()
        else:
            return

    def p(self):
        print("o sghid")
class RequestBack(QObject):
    finished = pyqtSignal()
    answer = pyqtSignal(bool)

    def run(self):
        for i in range(1):
            time.sleep(1)
            print(i)
        self.answer.emit(True)
        for i in range(1):
            time.sleep(1)
            print(i)
        self.finished.emit()

class ChatBack():
    pass


class Chatroom(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        intro_text = QLabel("""DAmmmm
        """)

        layout.addWidget(intro_text)
        
        components = [intro_text]
        
        for c in components:
            c.setAlignment(Qt.AlignCenter)
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #self.continue_button.setStyleSheet("")

        layout.setContentsMargins(200, 100, 200, 100)
        self.setLayout(layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    #first scene
    window = Scene()
    #window.intro()

    window.intro()
    #window.send_request()
    window.show()    
    
    sys.exit(app.exec_())
    