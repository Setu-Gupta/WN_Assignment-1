#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/time.h>

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

        struct timeval cur_time;
        if(gettimeofday(&cur_time, NULL))
        {
                printf("Failed to get current time! Exiting...\n");
                exit(-1);
        }

        unsigned long long time_usec = ((unsigned long long)cur_time.tv_sec * 1000000) + (unsigned long long)cur_time.tv_usec; 
        printf("Current time in micro_seconds: %lld\n", time_usec);

        return 0;
}
