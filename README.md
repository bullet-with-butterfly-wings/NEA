# Encryption Engine
This Encryption Engine was developed as a part of an NEA project for A-Level and GSCE students. The app implements symmetric and assymmetric protocols (RSA, Diffie Hellman Key Exchange with Feistel or Vernam cipher) on the local network, so two distinct device can communicate securely. It has two versions - one for Windows and one for Linux. The only dependency is the python library PyQt5.

## Installation
1. Download the repository from the GitHub repository.
2. Open the folder with your OS
3. Open terminal and type "pip install PyQt5" to download PyQt5 library.
4. You will connect to a server with IP in IP.txt. 
If nobody hasn't started the server, you will automatically start server with your own device and your IP is stored in IP.txt  
4. Run the main.py or Encryption Engine.exe (win).

## Good to know
All keys used for the encryption are stored in keys.txt.

If you got error regarding "already used IP", either go to your task manager and kill the app or type command "pkill python" into terminal.

If it doesn't work just restart it :3 (reboot if u r desperate)

## Built With
Python - libraries socket, PyQt5 and threading

C - customized library for encryption protocols with makefile

## Contacts
urmum@onlyfans.com
