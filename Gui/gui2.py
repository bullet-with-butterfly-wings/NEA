import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore

class EncryptionEngine(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        title_label = QLabel("First of all you need to connect!")
        text_label = QLabel("Text goes here")

        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")
        button4 = QPushButton("Button 4")
        buttons = [button1,button2,button3,button4]
        active_label = QLabel("People active:")
        active_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        v_layout2 = QVBoxLayout()
        v_layout2.addWidget(active_label)
        contact_buttons = []
        for _ in range(5):
            contact_buttons.append(QPushButton("Hey"))
            contact_buttons[-1].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            v_layout2.addWidget(contact_buttons[-1])

        for b in buttons:
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            b.resize(200,200)

        # Create grid layout and add widgets
        h_layout = QHBoxLayout()

        v_layout = QVBoxLayout()
        v_layout.addWidget(title_label)
        v_layout.addWidget(text_label)
        
        continue_button = QPushButton("Continue")
        continue_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #continue_button.setAlignment(QtCore.Qt.AlignCenter)
        grid = QGridLayout()
        grid.addWidget(button1, 2, 0)
        grid.addWidget(button2, 2, 1)
        grid.addWidget(button3, 3, 0)
        grid.addWidget(button4, 3, 1)
        v_layout.addLayout(grid)
        v_layout.addWidget(continue_button, alignment=QtCore.Qt.AlignCenter)
        h_layout.addLayout(v_layout)
        h_layout.addLayout(v_layout2)
        

        # Set layout
        self.setLayout(h_layout)

        # Set window properties
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle("Encryption Engine")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncryptionEngine()
    window.show()
    sys.exit(app.exec_())
