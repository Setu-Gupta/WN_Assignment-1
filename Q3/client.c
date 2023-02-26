#include <stdio.h>
#include <stdlib.h>

void print_usage()
{
        printf("Incorrect usage. Exiting!\n");
        printf("Usage: client <IP> <port>\n");
        exit(-1);
}

int main(int argc, char* argv[])
{
        if(argc < 3)
                print_usage();

        printf("Client starting...\n");
        printf("Contacting server at %s at port number %s\n", argv[1], argv[2]);
        return 0;
}
