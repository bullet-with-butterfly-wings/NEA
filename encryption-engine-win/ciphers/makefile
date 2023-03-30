CC = gcc
CFLAGS = -O2

SRCS = $(wildcard src/*.c)
LIB_OBJS = $(wildcard lib/*.c)

all: dh generator feistel rsa vernam

%: src/%.c
	$(CC) $(CFLAGS) $^ $(LIB_OBJS) -lpthread -lm -o bin/$@.exe

clean:
	$(RM) -r bin/*
