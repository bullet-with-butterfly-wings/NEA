import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class EncryptionGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets
        plaintext_label = QLabel("Plaintext:")
        self.plaintext_edit = QLineEdit()
        key_label = QLabel("Key:")
        self.key_combo = QComboBox()
        self.key_combo.addItems(["Key 1", "Key 2", "Key 3"])
        self.key_combo.setEditable(True)
        encrypt_button = QPushButton("Encrypt")
        encrypt_button.clicked.connect(self.encrypt_text)
        self.encrypted_label = QLabel("Encrypted:")
        self.encrypted_text = QTextEdit()
        self.description_label = QLabel("Description:")
        self.description_text = QTextEdit()
        
        protocol1_button = QPushButton("Protocol 1")
        protocol2_button = QPushButton("Protocol 2")
        protocol3_button = QPushButton("Protocol 3")
        protocol1_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        protocol2_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        protocol3_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        

        ip_label = QLabel("IP Address:")
        self.ip_edit = QLineEdit()

        # Create layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(plaintext_label)
        h_layout.addWidget(self.plaintext_edit)
        h_layout.addWidget(key_label)
        h_layout.addWidget(self.key_combo)
        h_layout.addWidget(encrypt_button)
        
        v_layout = QVBoxLayout()
        #v_layout.addLayout(h_layout)
        v_layout.addWidget(self.encrypted_label)
        v_layout.addWidget(self.encrypted_text)
        v_layout.addWidget(self.description_label)
        v_layout.addWidget(self.description_text)
        
        grid_layout = QGridLayout()
        grid_layout.addWidget(protocol1_button, 0, 0)
        grid_layout.addWidget(protocol2_button, 1, 0)
        grid_layout.addWidget(protocol3_button, 2, 0)
        h_layout2 = QHBoxLayout()
        h_layout2.addLayout(grid_layout)
        h_layout2.addLayout(v_layout)
        v_layout2 = QVBoxLayout()
        v_layout2.addWidget(ip_label)
        
        v_layout2.addLayout(h_layout)
        v_layout2.addWidget(self.ip_edit)
        v_layout2.addLayout(h_layout2)
        protocol1_button.clicked.connect(self.set_protocol)
        protocol2_button.clicked.connect(self.set_protocol)
        protocol3_button.clicked.connect(self.set_protocol)
        
        # Set the layout and window properties
        self.setLayout(v_layout2)
        self.setWindowTitle("Encryption Engine")
        self.setGeometry(200, 200, 1000, 700)

        # Set the blue theme
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0, 120, 255))
        self.setPalette(palette)


    def encrypt_text(self):
        # Get the plaintext, key, and chosen protocol
        plaintext = self.plaintext_edit.text()
        key = self.key_combo.currentText()
        protocol = self.sender().text()
        print(protocol)

        # TODO: Implement the encryption here
        encrypted = "encrypted"
        description = "Description of {}".format(protocol)

        # Update the encrypted text and description fields
        self.encrypted_text.setText(encrypted)
        self.description_text.setText(description) # it is not here yet => crash


    def set_protocol(self):
        protocol = self.sender().text()
        self.key_combo.setCurrentText(protocol)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = EncryptionGUI()
    gui.show()
    sys.exit(app.exec_())

