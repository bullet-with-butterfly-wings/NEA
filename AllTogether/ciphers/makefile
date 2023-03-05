all: numbers.o sha256.o library.a generator feistel rsa vernam dh
	
library.a: lib/sha256.c lib/numbers.c 
	ar rcs lib/library.a lib/numbers.o lib/sha256.o

generator: generator.c
	gcc -o generator generator.c lib/library.a -lpthread -lm

feistel: feistel.c
	gcc -o feistel feistel.c lib/library.a -lpthread -lm

rsa: rsa.c
	gcc -o rsa rsa.c lib/library.a -lpthread -lm

dh: dh.c
	gcc -o dh dh.c lib/library.a -lpthread -lm

numbers.o: lib/numbers.c lib/library.h 
	gcc -c -o lib/numbers.o lib/numbers.c

sha256.o: lib/sha256.c lib/library.h
	gcc -c -o lib/sha256.o lib/sha256.c

vernam: vernam.c
	gcc -o vernam vernam.c

clean: 
	rm lib/*.o
	rm feistel generator rsa vernam dh
