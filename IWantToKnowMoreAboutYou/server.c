#include <stdio.h>
#include <stdlib.h>

void hmm() {
    printf("flag{rop_this_rop_that_roppppp}\n");
}

void greet() {
    char buf[0x20];

    printf("Hello! What's your favorite dinosaur?\n");
    fgets(buf, 0x40, stdin);
    printf("Oh, I also love %s!\n", buf);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    greet();

    return 0;
}
