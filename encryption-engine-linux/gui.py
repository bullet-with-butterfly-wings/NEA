
import sys
from subprocess import call
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * 

def CssLoader(filename):
    with open(filename, "r") as rd:
        content = rd.read()
        rd.close()
    return content

converter = {"Feistel":"Feistel Cipher", "RSA":"RSA protocol", "DH":"Diffie-Hellman Key Exchange", "Vernam":"Vernam Cipher"}

class Scene(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1800, 1000)
        self.partner = -1
        icon = QIcon()
        pixmap = QPixmap("img/icon2.png")
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.decision = None
        self.protocols = ["",""]
        self.symm_key = ""
        self.setStyleSheet(CssLoader("design.css"))
        self.setWindowTitle("Encryption Engine")
        self.intro()
        
    def intro(self):
        self.state = "intro"
        self.sc = Intro()
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.setCentralWidget(self.sc) 
        self.sc.continue_button.clicked.connect(lambda: setattr(self,"state", "making_request"))
        self.show()

    def making_request(self, contacts):
        self.state = "making_request"
        self.sc = RequestMaker(contacts)
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.setCentralWidget(self.sc)
        pro_buttons = [self.sc.feistel_button, self.sc.rsa_button, self.sc.dh_button,  self.sc.vernam_button]
        titles = ["Feistel", "RSA", "DH", "Vernam"]
        
        for i in range(len(pro_buttons)):
            pro_buttons[i].clicked.connect(lambda idk, arg = (i, pro_buttons[i], pro_buttons[len(titles)-1-i]): self.protoco(titles[arg[0]], arg[1],arg[2]))
            pro_buttons[i].setCheckable(True)
        
        self.sc.send_button.setEnabled(False)
        self.sc.send_button.clicked.connect(lambda: self.waiting_for_response())#send request
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
                else:
                    contact_buttons[i].setChecked(False)
                    
        if (self.protocols[0] != "" and self.protocols[1] != "") and contacts_ready:
            self.sc.send_button.setEnabled(True)
        else:
            self.sc.send_button.setEnabled(False)
        
    def protoco(self, pro, button, uncheck_button):
        i = int(pro in ["Vernam", "Feistel"])
        if not button.isChecked():
            self.protocols[i] = ""
        else: 
            self.protocols[i] = pro
            uncheck_button.setChecked(False)
        
        c_ready = False
        for c in contact_buttons:
            if c.isChecked():
                c_ready = True 

        if (self.protocols[0] != "" and self.protocols[1] != "") and c_ready:
            self.sc.send_button.setEnabled(True)
        else:
            self.sc.send_button.setEnabled(False)

    def chatroom(self):
        self.setWindowTitle("Encrypted Channel")
        self.state = "chatroom"
        self.sc = Chatroom()
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.setCentralWidget(self.sc)
        self.sc.send_button.clicked.connect(self.send_message)
    
    def send_message(self):
        self.plainText = self.sc.text_edit.toPlainText()
        f = open("buffer.txt", "w")
        f.write(self.plainText)
        f.close()
        if self.protocols[1] == "Vernam":
            print("Ciphering")
            call(["./ciphers/bin/vernam", self.symm_key])
            print("Key",self.symm_key)
        else:
            print("Ciphering")
            call(["./ciphers/bin/feistel","1",self.symm_key])
            print("Key",self.symm_key)
        f = open("buffer.txt", "r")
        self.cipherText = f.read()
        f.close()
        self.sc.text_display.append(f"You  PlainText:{self.plainText} \n     CipherText: {self.cipherText}")
        self.state = "sending"

    def response(self, partner, suggested_pro):
        self.state = "recieved_request"
        self.sc = RequestReciever("("+partner[0]+" "+str(partner[1])+")", " ".join(suggested_pro))
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.setCentralWidget(self.sc)
        self.sc.accept_button.clicked.connect(lambda: (setattr(self, "decision", True), setattr(self, "state", "answered_request")))
        self.sc.reject_button.clicked.connect(lambda: (setattr(self, "decision", False), setattr(self, "state", "answered_request")))
        self.show()
    
    def waiting_for_response(self):
        self.state = "waiting_for_response"
        self.sc = Waiting()
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.setCentralWidget(self.sc)
        self.show()
    
    def dh(self, next): 
        self.sc = DH()
        self.setWindowTitle("Diffie-Hellman protocol")
        self.setCentralWidget(self.sc)
        self.sc.setStyleSheet(CssLoader("design.css"))
        
        if next == "Feistel":
            self.sc.continue_button.clicked.connect(self.feistel)
        else:
            self.sc.continue_button.clicked.connect(self.vernam)
        self.show()


    def rsa(self, next): 
        self.sc = RSA()
        self.setWindowTitle("RSA protocol")
        self.setCentralWidget(self.sc)
        self.sc.setStyleSheet(CssLoader("design.css"))
        
        if next == "Feistel":
            self.sc.continue_button.clicked.connect(self.feistel)
        else:
            self.sc.continue_button.clicked.connect(self.vernam)
        self.show()

    def feistel(self): 
        self.sc = Feistel(self)
        self.setWindowTitle("Feistel Cipher")
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.setCentralWidget(self.sc)
        self.show()

    def vernam(self): 
        self.sc = Vernam(self)
        self.setWindowTitle("Vernam Cipher")
        self.setCentralWidget(self.sc)
        self.sc.setStyleSheet(CssLoader("design.css"))
        self.show()
            
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Return and self.state == "chatroom":
            self.send_message()

class Intro(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        intro_text = QLabel("""Welcome to my encryption engine!

        With this app, you will establish communication through a secure channel between two devices on a local area network (LAN). 
    
    You have two possibilities now:
        """)
        intro_text.setWordWrap(True)
        wait_text = QLabel("or you can wait for someones request...")
        self.continue_button = QPushButton("Request",self)

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

class Vernam(QWidget):
    def __init__(self, win) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        text1_label = QLabel("""The decryption process in the Vernam cipher is essentially the same as the encryption process. The receiver combines each character of the encrypted message with the corresponding character of the key using modular subtraction to recover the original plaintext message.
The security of the Vernam cipher is based on the randomness and secrecy of the key. If the key is generated randomly and used only once, it is impossible for an attacker to decrypt the message without the key. However, if the key is reused or not truly random, the security of the cipher is compromised.""")
        text1_label.setWordWrap(True) # wrap text if too long
        
        # create QLabel for picture
        picture_label = QLabel(self)
        #https://medium.com/@gmhpwx/cipher-types-e6b8e746d610
        picture = QPixmap("img/vernam.jpg").scaled(int(1356*0.7),int(549*0.7)) 
        picture_label.setPixmap(picture)
        picture_label.setAlignment(Qt.AlignRight)
        
        text2_label = QLabel("""The Vernam cipher, also known as the one-time pad, is a classic encryption algorithm that has been used in various applications since its invention in 1917. It is considered to be the only encryption method that is mathematically unbreakable, provided that the key is truly random and used only once.
The encryption process in the Vernam cipher involves combining each character of the plaintext message with the corresponding character of the key using modular addition. This means that each character of the plaintext is shifted by the corresponding character in the key. For example, if the plaintext message is "HELLO" and the key is "WORLD", then the first letter "H" would be shifted by "W", the second letter "E" would be shifted by "O", and so on.""")
        text2_label.setWordWrap(True) # wrap text if too long
        # create QPushButton for continue button
        self.continue_button = QPushButton("Continue",self)
        hbox = QHBoxLayout()
        hbox.addWidget(text1_label)
        hbox.addWidget(picture_label)
        
        # create QVBoxLayout and add widgets to it
        vbox = QVBoxLayout()
        vbox.addWidget(text2_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.continue_button)
        
        # set layout of widget to the QVBoxLayout
        components = [self.continue_button,text1_label, text2_label]
        
        for c in components[1:]:
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.continue_button.clicked.connect(win.chatroom)
        #self.continue_button.setStyleSheet("")
        self.setLayout(vbox)
        
        
class Feistel(QWidget):
    def __init__(self,win) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        text1_label = QLabel("""The Feistel cipher is a symmetric encryption algorithm that uses a combination of substitution and transposition to encrypt plaintext messages. It is named after Horst Feistel, who first described the concept in 1973.
In a Feistel cipher, the plaintext message is divided into two halves, and each half goes through a series of rounds where they are transformed using a subkey derived from the main key. The transformation involves substitution and permutation operations, which change the order and values of the bits in the data. After each round, the two halves are swapped, and the process repeats for a set number of rounds until the final ciphertext is produced.
""") 
        text1_label.setWordWrap(True) # wrap text if too long
        
        # create QLabel for picture
        picture_label = QLabel(self)
        #https://asecuritysite.com/symmetric/fei
        picture = QPixmap("img/feistel.png").scaled(int(621*1.4),int(481*1.4)) # replace "rsa_diagram.png" with your image file name and path
        picture_label.setPixmap(picture)
        picture_label.setAlignment(Qt.AlignRight)
        
        text2_label = QLabel("""The security of the Feistel cipher is based on the fact that each round uses a different subkey, which makes it difficult for an attacker to derive the main key from the ciphertext. Additionally, the use of substitution and permutation operations makes the cipher resistant to various types of attacks, such as brute force attacks and statistical attacks.
Feistel ciphers have been used in a variety of applications, including the Data Encryption Standard (DES) and the Advanced Encryption Standard (AES). They are also used in various block cipher modes, such as Cipher Block Chaining (CBC) and Cipher Feedback (CFB).""")
        text2_label.setWordWrap(True) # wrap text if too long
        # create QPushButton for continue button
        self.continue_button = QPushButton("Continue",self)
        hbox = QHBoxLayout()
        hbox.addWidget(text2_label)
        hbox.addWidget(picture_label)
        
        # create QVBoxLayout and add widgets to it
        vbox = QVBoxLayout()
        vbox.addWidget(text1_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.continue_button)
        
        # set layout of widget to the QVBoxLayout
        components = [self.continue_button,text1_label, text2_label]
        
        self.continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.continue_button.setStyleSheet("")
        self.continue_button.clicked.connect(win.chatroom)
        for c in components[1:]:
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(vbox)


class RSA(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCipheringCenter)
        text1_label = QLabel("""RSA encryption is based on the mathematics of modular arithmetic and prime factorization. The basic idea behind RSA encryption is to use a pair of keys, one for encryption and one for decryption, that are mathematically related but cannot be easily reversed. The public key is used for encryption, and it is generated by multiplying two large prime numbers. The private key, which is kept secret, is generated by finding the modular multiplicative inverse of a certain value with respect to the product of the two primes.""")
        text1_label.setWordWrap(True) # wrap text if too long
        
        # create QLabel for picture
        picture_label = QLabel(self)
        #https://www.tutorialspoint.com/cryptography/public_key_encryption.htm
        picture = QPixmap("img/rsa.jpg") 
        picture_label.setPixmap(picture)
        picture_label.setAlignment(Qt.AlignRight)
        
        text2_label = QLabel("""To encrypt a message, it is first converted into a numerical value and then raised to the power of the public key, with the result being taken modulo the product of the two primes. This produces the encrypted message, which can only be decrypted with the corresponding private key. To decrypt the message, the recipient raises the encrypted message to the power of the private key, again modulo the product of the two primes, which recovers the original numerical value of the message.
The security of RSA encryption is based on the fact that factoring large composite numbers into their prime factors is a computationally difficult problem. Therefore, it is difficult for an attacker to determine the private key from the public key and the encrypted message. The security of RSA encryption relies on the fact that it is difficult to factorize large composite numbers into their prime factors, which makes it one of the most widely used encryption algorithms in modern cryptography.""")
        text2_label.setWordWrap(True) # wrap text if too long
        text2_label.setWordWrap(True)
        # create QPushButton for continue button
        self.continue_button = QPushButton("Continue",self)
        hbox = QHBoxLayout()
        hbox.addWidget(text2_label)
        hbox.addWidget(picture_label)
        
        # create QVBoxLayout and add widgets to it
        vbox = QVBoxLayout()
        vbox.addWidget(text1_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.continue_button)
        
        # set layout of widget to the QVBoxLayout
        self.setLayout(vbox)
        components = [self.continue_button,text1_label, text2_label]
        
        for c in components[1:]:
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.continue_button.setStyleSheet("")

        #layout.setContentsMargins(200, 200, 200, 200)
        
class DH(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        text1_label = QLabel("""The security of the Diffie-Hellman cipher is based on the difficulty of computing discrete logarithms in a finite field. In other words, given a large prime number and a generator, it is difficult to compute the logarithm of a number with respect to that generator. This means that even if an attacker intercepts the public keys being transmitted over the public channel, they cannot easily compute the shared secret key without knowing the private keys of both parties.

The Diffie-Hellman cipher is widely used in various protocols, such as secure shell (SSH), internet protocol security (IPsec), and secure sockets layer (SSL) to establish a secure communication channel between two parties.""")
        text1_label.setWordWrap(True) # wrap text if too long
        
        # create QLabel for picture
        picture_label = QLabel(self)
        # https://www.researchgate.net/figure/Block-diagram-of-the-Diffie-Hellman-algorithm_fig1_349609600
        picture = QPixmap("img/dh.png") # replace "rsa_diagram.png" with your image file name and path
        picture_label.setPixmap(picture)
        picture_label.setAlignment(Qt.AlignRight)
        
        text2_label = QLabel("The Diffie-Hellman cipher is a method of securely exchanging cryptographic keys over a public channel. It was invented by Whitfield Diffie and Martin Hellman in 1976. The basic idea behind the Diffie-Hellman cipher is to use modular arithmetic to exchange keys between two parties without ever transmitting the key over the public channel. Instead, each party generates a public key and a private key, and then shares the public key with the other party. Each party then uses their own private key and the other party's public key to compute a shared secret key. This shared key can then be used for symmetric encryption and decryption.")
        text2_label.setWordWrap(True)
        self.continue_button = QPushButton("Continue",self)
        hbox = QHBoxLayout()
        hbox.addWidget(text1_label)
        hbox.addWidget(picture_label)
        
        # create QVBoxLayout and add widgets to it
        vbox = QVBoxLayout()
        vbox.addWidget(text2_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.continue_button)
        
        # set layout of widget to the QVBoxLayout
        self.setLayout(vbox)
        components = [self.continue_button,text1_label, text2_label]
        
        for c in components[1:]:
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.continue_button.setStyleSheet("")

        #layout.setContentsMargins(200, 200, 200, 200)
        
class RequestMaker(QWidget):
    def __init__(self, contacts) -> None:
        super().__init__()
        label = QLabel("Pick one assymmetric and symmetric protocol + your communication buddy:")
        label.setAlignment(Qt.AlignCenter)

        # Create pro_buttons
        self.rsa_button = QPushButton(converter["RSA"])
        self.rsa_button.setMinimumSize(QSize(80, 40))
        self.dh_button = QPushButton(converter["DH"])
        self.dh_button.setMinimumSize(QSize(80, 40))
        self.vernam_button = QPushButton(converter["Vernam"])
        self.vernam_button.setMinimumSize(QSize(80, 40))
        self.feistel_button = QPushButton(converter["Feistel"])
        self.feistel_button.setMinimumSize(QSize(80, 40))

        self.send_button = QPushButton("Send")
        self.send_button.setMinimumSize(QSize(80, 40))
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumSize(QSize(80, 40))

        #self.rsa_button.clicked.connect(self.)
        #self.dh_button.clicked.connect(self.self.dh_button)

        # Create a grid layout and add pro_buttons and label
        layout = QGridLayout()
        layout.setSpacing(20)
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(QLabel( 
     """        Asymmetric encryption uses a pair of keys - 
        a public key for encryption and a private key for decryption. 
        Asymmetric encryption is typically used to establish a secure communication channel 
        between two parties, as the public keys can be freely shared and used to encrypt messages.""", self), 1, 0, 1, 2)
        layout.addWidget(self.rsa_button, 2, 0)
        layout.addWidget(self.dh_button, 2, 1)
        layout.addWidget(QLabel(
     """        Once the secure communication channel is established,
        symmetric encryption is used for the rest of the conversation. Symmetric encryption 
        uses the same key for encryption and decryption, making it more efficient 
        than asymmetric encryption. However, the key must be kept secret to maintain 
        the security of the communication.""", self), 3, 0, 1, 2)
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
            contact_buttons[-1].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            #contact_buttons[-1].setWordWrap(True)
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
        self.label = QLabel("Waiting for the decision")
        self.label.setFont(QFont("Ariel",2000))
        self.label.setAlignment(Qt.AlignCenter)            
        self.decision = QLabel("After the respond, the app will forward you to the corresponding interface.")
        self.decision.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.decision)
        layout.setContentsMargins(200, 100, 200, 100)
        self.setLayout(layout)


class RequestReciever(QWidget):
    def __init__(self, source, suggested_pro) -> None:
        super().__init__()
        # Create a label to display the request message
        suggested_pro = suggested_pro.split(" ")
        self.request_label = QLabel(f"""You have received a request from {source}  for the following protocols: \n 
        Assymmetric:{converter[suggested_pro[0]]}              Symmetric:{converter[suggested_pro[1]]}""")
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

class Chatroom(QWidget):
    def __init__(self):
        super().__init__()
        # Create the text edit widget for displaying messages
        self.text_display = QTextEdit("Messages:")
        self.text_display.setFont(QFont("Arial", 15))
        self.text_display.setReadOnly(True)
        #self.text_display.setFontSize(23)
        self.text_edit = QTextEdit("Type in your message")

        # Create the "Send" button
        self.send_button = QPushButton("Send")
        
        # Create a vertical layout to hold the text edit and send button
        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.send_button)


        self.setLayout(layout)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    #first scene
    window = Scene()
    window.intro()
    #window.send_request()
    window.show()    
    
    sys.exit(app.exec_())
    