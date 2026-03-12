#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));

    struct {
        char name[0x20];
        unsigned long long luck;
    } locals;

    locals.luck = (((long long)rand() << 0x20) | rand()) % 0xCAFEBABE + 1;
    printf("Hi! What's your name: ");
    fgets(locals.name, 0x30, stdin);

    if(locals.luck == 0xDEADBEEF) {
        printf("Congrats! You're super duper lucky!!!\n");
        system("cat flag.txt");
    } else {
        printf("You've got bad luck! Better luck next time!\n");
    }

    return 0;
}
