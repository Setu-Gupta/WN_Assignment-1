#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <unistd.h>

void print_usage()
{
        fprintf(stderr, "Incorrect usage. Exiting!\n");
        printf("Usage: client <IP> <port>\n");
        exit(-1);
}

int main(int argc, char* argv[])
{
        // Sanitize the user arguments
        if(argc < 3)
                print_usage();
        
        printf("Client starting...\n");
        printf("Contacting server at %s at port number %s\n", argv[1], argv[2]);

        // Create the client socket
        int sock_fd;
        if((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
                fprintf(stderr, "Failed to create socket! Exiting...\n");
                exit(-1);
        }

        // Create the structure to describe the server
        struct sockaddr_in server;
        server.sin_family = AF_INET;
        server.sin_port = htons((unsigned short) strtoul(argv[2], NULL, 10));
        if(inet_pton(AF_INET, argv[1], &server.sin_addr) <= 0)
        {
                fprintf(stderr, "Could not parse the IP address! Exiting...\n");
                exit(-1);
        }
        
        // Establish connection with the server
        if(connect(sock_fd, (struct sockaddr*)&server, sizeof(server)) < 0)
        {
                fprintf(stderr, "Could not connect to the server! Exiting...\n");
                exit(-1);
        }

        // Send the time stamp 100 times
        for(int i = 0; i < 100; i++)
        {
                // Get the current clock time
                struct timeval cur_time;
                if(gettimeofday(&cur_time, NULL))
                {
                        fprintf(stderr, "Failed to get current time! Exiting...\n");
                        exit(-1);
                }
                unsigned long long time_usec = ((unsigned long long)cur_time.tv_sec * 1000000) + (unsigned long long)cur_time.tv_usec; 
                
                if(send(sock_fd,  &time_usec, sizeof(time_usec), 0) < 0)
                {
                        fprintf(stderr, "Failed to send the time stamp! Exiting...\n");
                        exit(-1);
                }
        }

        // Close the file descriptor
        close(sock_fd);

        printf("Exiting...\n");
        return 0;
}
