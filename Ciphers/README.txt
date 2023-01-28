gcc -o encrypting encrypting.c library.c for compiling with library

order of variables n, d, e, m

Seperate file to put aside messages (DH, RSA, ...) ???

C doesnt permit array with size defined by variable => conses about block size 64 so one half fits into hash XOR + 8 (to fit SHA)


https://stackoverflow.com/questions/2262386/generate-sha256-with-openssl-and-c
SHA is bullshit, and it needs special compilation: gcc -Wall -g -o program Playground.c -lcrypto (Fuck)

gcc -o DH DH.o library.o -lpthread -lm and -c flag for libraries