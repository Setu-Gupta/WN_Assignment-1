CC = gcc
CFLAGS = -Werror -Wall -Wextra -pedantic -march=native -Ofast

all: server client

server: server.c
	$(CC) $(CFLAGS) $< -o $@

client: client.c
	$(CC) $(CFLAGS) $< -o $@

.PHONY: clean
clean:
	rm -rf server client
