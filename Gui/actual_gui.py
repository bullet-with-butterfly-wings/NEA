import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 1000, 700)
        self.setWindowTitle("Encryption Engine")

    def intro(self):
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        continue_button = QPushButton("Connect")
        intro_text = QLabel("""Welcome to the Encryption Engine, 
        a tool developed specifically for students to learn 
        about ciphers and their applications. 
        You have two possibilities now:
        """)
        wait_text = QLabel("or you can wait for someones request...")
        components = [continue_button,intro_text,wait_text]
        #layout.setRowStretch(5, 10)
        #layout.setRowStretch(1, 4)

        #v_layout.addStretch()
        layout.addWidget(intro_text )
        layout.addWidget(continue_button)
        layout.addWidget(wait_text)
        
        for c in components[1:]:
            c.setAlignment(Qt.AlignCenter)
            c.setStyleSheet("border: 1px solid black;padding-left: 100px; padding-right: 100px")
            c.setFont(QFont("Ariel", 20))


            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #continue_button.setStyleSheet("")

        layout.setContentsMargins(200, 100, 200, 100)
        continue_button.setFont(QFont("Ariel", 20))
        self.setLayout(layout)

    def response_to_request(self, request_from, protocols):

        self.setWindowTitle("Request")

        # Create a label to display the request message
        request_label = QLabel("You have received a request from " + request_from + " for the following protocols: " + protocols)
        request_label.setAlignment(Qt.AlignCenter)
        request_label.setMargin(20)

        # Create the accept button
        accept_button = QPushButton("Accept")
        accept_button.setStyleSheet("background-color: green")

        # Create the reject button
        reject_button = QPushButton("Reject")
        reject_button.setStyleSheet("background-color: red")


        reject_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        accept_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        request_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Create a horizontal layout to hold the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(accept_button)
        buttons_layout.addWidget(reject_button)
        buttons_layout.setContentsMargins(20, 0, 20, 20)

        # Create a widget to hold the layout
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        # Set the layout of the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(request_label)
        main_layout.addWidget(buttons_widget)
        main_layout.setContentsMargins(200, 100, 200, 100)

        self.setLayout(main_layout)

    def send_request(self):
        label = QLabel("Select a protocols:")
        label.setAlignment(Qt.AlignCenter)

        # Create buttons
        rsa_button = QPushButton("RSA")
        rsa_button.setMinimumSize(QSize(80, 40))
        dh_button = QPushButton("Diffie-Hellman")
        dh_button.setMinimumSize(QSize(80, 40))
        vernam_button = QPushButton("Vernam")
        vernam_button.setMinimumSize(QSize(80, 40))
        feistel_button = QPushButton("Feistel")
        feistel_button.setMinimumSize(QSize(80, 40))

        send_button = QPushButton("Send")
        send_button.setMinimumSize(QSize(80, 40))
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumSize(QSize(80, 40))

        contacts_button1 = QPushButton("Contact 1")
        contacts_button1.setMinimumSize(QSize(80, 40))
        contacts_button2 = QPushButton("Contact 2")
        contacts_button2.setMinimumSize(QSize(80, 40))
        contacts_button3 = QPushButton("Contact 3")
        contacts_button3.setMinimumSize(QSize(80, 40))
        contacts_button4 = QPushButton("Contact 4")
        contacts_button4.setMinimumSize(QSize(80, 40))

        # Create a grid layout and add buttons and label
        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(QLabel("Assymetric encryption...", self), 1, 0, 1, 2)
        layout.addWidget(rsa_button, 2, 0)
        layout.addWidget(dh_button, 2, 1)
        layout.addWidget(QLabel("Symetric encryption...", self), 3, 0, 1, 2)
        layout.addWidget(vernam_button, 4, 0)
        layout.addWidget(feistel_button, 4, 1)
        layout.addItem(QSpacerItem(0, 20), 5, 0, 1, 2)
        layout.addWidget(send_button, 6, 1)
        layout.addWidget(cancel_button, 6, 0)

        # Create a separate vertical layout for contacts buttons
        contacts_layout = QVBoxLayout()

        contacts_layout.addWidget(contacts_button1)
        contacts_layout.addWidget(contacts_button2)
        contacts_layout.addWidget(contacts_button3)
        contacts_layout.addWidget(contacts_button4)
        contacts_layout.setContentsMargins(0, 0, 0, 0)


        layout.addLayout(contacts_layout, 0, 2, 7, 1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)


    
        layout.setContentsMargins(20, 50, 10, 50)
        self.setLayout(layout)


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #first scene
    window = Scene()
    #window.response_to_request("john","https")
    #window.intro()
    window.send_request()
    window.show()
    
    sys.exit(app.exec_())
    