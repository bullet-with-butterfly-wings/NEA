CC = gcc
CFLAGS = -O2

SRCS = $(wildcard src/*.c)
OBJS = $(patsubst src/%.c, obj/%.o, src)

LIB_OBJS = lib/numbers.o lib/sha256.o

BIN = dh generator feistel rsa vernam

all: $(BIN)

.PRECIOUS: obj/%.o

#binary
%: obj/%.o lib/library.a 
	$(CC) $(CFLAGS) -o bin/$@ src/$(notdir $@).c -L./lib -lrary -lpthread -lm
	$(CC) $(CFLAGS) -o dbg/$@.out src/$(notdir $@).c -L./lib -lrary -lpthread -lm -g

obj/%.o: src/%.c
	$(CC) $(CFLAGS) -c $^ -lpthread -lm -o $@

#debug


#library
lib/library.a: $(LIB_OBJS) 
	ar rcs lib/library.a $(LIB_OBJS)

lib/%.o: lib/%.c
	$(CC) $(CFLAGS) -c $^ -lm -lmthread -o $@

#deleting
clean: 
	$(RM) -r bin/* obj/*
	rm lib/*.o
	rm lib/library.a

#tests - do not work
test_vernam: vernam
	echo "start" > buffer.txt
	echo "sucux" > correct.txt
	echo "abcdefghij" > input.txt 
	echo "abcdefghij" | ./bin/vernam
	diff buffer.txt correct.txt || (echo "Test failed" && exit 1)
