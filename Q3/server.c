#include <stdio.h>
#include <stdlib.h>

void print_usage()
{
        printf("Incorrect usage. Exiting!\n");
        printf("Usage: server <port>\n");
        exit(-1);
}

int main(int argc, char* argv[])
{
        if(argc < 2)
                print_usage();

        printf("Server starting at port %s...\n", argv[1]);
        return 0;
}
