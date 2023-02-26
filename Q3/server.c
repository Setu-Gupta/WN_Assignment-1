#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <unistd.h>
#include <netinet/in.h>

void print_usage()
{
        printf("Incorrect usage. Exiting!\n");
        printf("Usage: server <port> <file>\n");
        exit(-1);
}

int main(int argc, char* argv[])
{
        // Sanitize the user arguments
        if(argc < 3)
                print_usage();

        printf("Server starting at port %s and dumping latency in %s...\n", argv[1], argv[2]);
        
        // Open the file to dump the latencies into
        FILE *dump;
        if((dump = fopen(argv[2], "w+")) == NULL)
        {
                fprintf(stderr, "Failed to open dumping file! Exiting...\n");
                exit(-1);
        }

        // Create the server socket
        int sock_fd;
        if((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
                fprintf(stderr, "Failed to create socket! Exiting...\n");
                exit(-1);
        }

        // Create the structure to describe the server
        struct sockaddr_in server;
        server.sin_family = AF_INET;
        server.sin_port = htons((unsigned short) strtoul(argv[1], NULL, 10));
        server.sin_addr.s_addr = INADDR_ANY;
        
        // Bind the socket to the specified port
        if(bind(sock_fd, (struct sockaddr*)&server, sizeof(server)) < 0)
        {
                fprintf(stderr, "Failed to bind socket! Exiting...\n");
                exit(-1);
        }

        // Start listening for connections
        if(listen(sock_fd, 0) < 0)
        {
                fprintf(stderr, "Failed to start listening! Exiting...\n");
                exit(-1);
        }
        
        // Accept the connection from the client
        int client_fd;
        struct sockaddr_in client;
        unsigned int client_size = sizeof(client);
        if((client_fd = accept(sock_fd, (struct sockaddr*)&client, &client_size)) < 0)
        {
                fprintf(stderr, "Failed to accept connection! Exiting...\n");
                exit(-1);
        }

        // Accept time stamp 100 times
        for(int i = 0; i < 100; i++)
        {
                // Read the client's time stamp
                unsigned long long client_timestamp;
                if(read(client_fd, &client_timestamp, sizeof(client_timestamp)) < 0)
                {
                        fprintf(stderr, "Failed to read data! Exiting...\n");
                        exit(-1);
                }
                
                // Get local time stamp
                struct timeval cur_time;
                if(gettimeofday(&cur_time, NULL))
                {
                        printf("Failed to get current time! Exiting...\n");
                        exit(-1);
                }
                unsigned long long time_usec = ((unsigned long long)cur_time.tv_sec * 1000000) + (unsigned long long)cur_time.tv_usec; 
                
                // Compute the latency
                unsigned long long latency_usec = time_usec - client_timestamp;
               
                // Display and dump the latency
                printf("Latency: %lld\n", latency_usec);
                fprintf(dump, "%lld\n", latency_usec);
        }

        // Close the client connection
        close(client_fd);

        // Shut the server down
        shutdown(sock_fd, SHUT_RDWR);

        // Close the dump file
        fclose(dump);
        
        printf("Exiting...\n");
        return 0;
}
