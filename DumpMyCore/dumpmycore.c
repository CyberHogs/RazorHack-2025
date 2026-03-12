#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>


char buf[2048] = { 0 };

int main() {
    int res = -1;
    int serv_fd = socket(AF_INET, SOCK_STREAM, 0);
    if(serv_fd < 0) {
        printf("Socket creation failed.\n");
        return -1;
    }

    int opt = 1;
    if(setsockopt(serv_fd, SOL_SOCKET, SO_KEEPALIVE | SO_REUSEADDR, &opt, sizeof(opt)) != 0) {
        printf("Setsockopt failed.\n");
        goto CLOSE_SERV;
    }

    struct sockaddr_in addr;
    socklen_t addrlen = sizeof(addr);
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(8080);

    if(bind(serv_fd, (struct sockaddr*)&addr, sizeof(addr)) != 0) {
        printf("Bind failed.\n");
        goto CLOSE_SERV;
    }

    if(listen(serv_fd, 1) != 0) {
        printf("Listen failed.\n");
        goto CLOSE_SERV;
    }

    int conn_fd = accept(serv_fd, (struct sockaddr*)&addr, &addrlen);
    if(conn_fd < 0) {
        printf("Accept connection failed.\n");
        goto CLOSE_SERV;
    }

    ssize_t valread = read(conn_fd, &(buf[1337]), 21);
    printf("flag{%s}", &buf[1337]);

    res = 0;
CLOSE_SERV:
    close(serv_fd);
CLOSE_CONN:
    close(conn_fd);

    return res;
}
