# Decode Me
This is supposed to be a basic reverse engineering challenge that needs some
sort of decompiler (or disassembler if you're hardcore) to solve, e.g.
BinaryNinja, Ghidra, IDA. The challenge is a basic input checker where the input
is the flag. 

Created by Tyr Rex.

<details>
    <summary>Flag</summary>
    <code>flag{t-rexes_r_my_favorite_ever}</code>
</details>

# Files Provided
- `decode_me`

# Tools
- Ghidra
- Python


# Steps to Solve
I used Ghidra for decompilation. It gives me
```
 1|undefined8 main(void) {
 2|    ulong local_a0;
 3|    byte local_98 [48];
 4|    byte local_68 [48];
 5|    byte local_38 [40];
 6|
 7|    local_10 = *(long *)(in_FS_OFFSET + 0x28);
 8|    local_98[0] = 0xe;
 9|    local_98[1] = 5;
10|    // ...
11|    local_98[0x1f] = 0x42;
12|    local_98[0x20] = 0;
13|    local_68[0] = 0x68;
14|    local_68[1] = 0x69;
15|    // ...
16|    local_68[0x1f] = 0x3f;
17|    local_68[0x20] = 0;
18|    printf("Enter the password: ");
19|    fgets((char *)local_38,0x21,stdin);
21|    local_a0 = 0;
22|    do {
23|        if (0x1f < local_a0) {
24|            printf("Correct Password! The tallest dinosaur is apparently called Sauroposeidon.");
25|    LAB_001012e0:
26|          return 0;
27|        }
28|        if (local_38[local_a0] != (local_68[local_a0] ^ local_98[local_a0])) {
29|            printf("Wrong Password!!!!!");
31|            goto LAB_001012e0;
32|        }
33|        local_a0 = local_a0 + 1;
34|    } while( true );
35|}
```

We can see that there are two initialized arrays, `local_98` and `local_68`, an
`fgets`, and a main loop. We see that the `fgets` input gets put into the
`local_38` variable. In the main loop, we see that the `local_38`, our input, is
getting compared to `local_68[local_a0] ^ local_98[local_a0]`. If they don't
match, we get a wrong password message. If they do match, which is when
`local_a0` becomes bigger than 31 (because the strings have a length of 32),
then we get a correct password message. This only happens if `local_38[local_a0]
== local_68[local_a0] ^ local_98[local_a0]` for all `0 <= local_a0 <= 31`.

So we just need to input the correct thing to get the correct password message.
We can just XOR each element in `local_68` and `local_98` with each other and
we'll get the correct input. Here's that in python
```python
a = list(map(ord, '\x0e\x05\x08\x0e\x12\x2b\x49\x1b\x01\x27\x1c\x1c\x2a\x2d\x2d\x18\x17\x00\x15\x15\x04\x06\x1c\x0e\x07\x3a\x30\x0b\x29\x08\x17\x42'))
b = list(map(ord, '\x68\x69\x69\x69\x69\x5f\x64\x69\x64\x5f\x79\x6f\x75\x5f\x72\x75\x6e\x5f\x73\x74\x72\x69\x6e\x67\x73\x5f\x6f\x6e\x5f\x6d\x65\x3f'))
print(''.join(f'{chr(a^b)}' for a, b in zip(b, a)))
```

which prints `flag{t-rexes_r_my_favorite_ever}`. we got the flag woohoo
