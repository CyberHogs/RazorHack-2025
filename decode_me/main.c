#include "stdio.h"

int main() {
    char a[] = "\x0e\x05\x08\x0e\x12\x2b\x49\x1b\x01\x27\x1c\x1c\x2a\x2d\x2d\x18\x17\x00\x15\x15\x04\x06\x1c\x0e\x07\x3a\x30\x0b\x29\x08\x17\x42";
    char b[] = "hiiii_did_you_run_strings_on_me?";
    char pass[33];

    printf("Enter the password: ");
    fgets(pass, 33, stdin);

    for(unsigned long int i = 0; i < 32; i++) {
        if(pass[i] != (a[i] ^ b[i])) {
            printf("Wrong Password!!!!!");
            return 0;
        }
    }

    printf("Correct Password! The tallest dinosaur is apparently called Sauroposeidon.");
}
