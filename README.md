# Encryption Engine
This Encryption Engine was developed as a part of my NEA project for A-Level and GSCE students. The app implements symmetric and asymmetric protocols (RSA, Diffie Hellman Key Exchange with Feistel or Vernam cipher) on the local network, so two different devices can communicate securely. It has two versions - one for Windows and one for Linux. The only dependency is the python library PyQt5.

## Installation
1. Download the repository from the GitHub repository.
2. Open the folder with your OS
3. Open the terminal and type "pip install PyQt5" to download the PyQt5 library.
4. You will connect to a server with IP in IP.txt. 
If nobody hasn't started the server, you will automatically begin the server with your device and your IP is stored in IP.txt  
4. Run the main.py or Encryption Engine.exe (win).

## Good to know
All keys used for the encryption are stored in keys.txt.

If you get an error regarding "already used IP, " go to your task manager and kill the app or type the command "pkill python" into the terminal.

If it doesn't work, just restart it :3 (reboot if u r desperate)

## Built With
Python - libraries socket, PyQt5 and threading

C - customized library for encryption protocols with makefile

## Contacts
urmum@onlyfans.com
