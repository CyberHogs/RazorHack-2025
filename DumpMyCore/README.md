# DumpMyCore
Created by Tyr Rex.

The server, `dumpmycore`, crashed right after receiving a message and generated a coredump,
`coredump.tar.gz`. We fortunately also have the source code for the server, `dumpmycore.c`. We know
that the client talking to the server looked similar to `client.py`, but we have no idea what it
sent. *Can you recover what the client sent to the server?*


<details>
    <summary>Flag</summary>
    <code>flag{my_c0r35_r_3v3rywh3r3}</code>
</details>

# Files Provided
- `coredump.tar.gz`
- `dumpmycore`
- `dumpmycore.c`
- `client.py`

# Tools
- GDB

# Steps to Solve

<details>
<summary>Steps to Solve</summary>

## Introduction

Looking at the source code in `dumpmycore.c`, we can see that the server writes what was sent
through the connection to `&(buf[1337])`.
```c
...
ssize_t valreaad = read(conn_fd, &(buf[1337]), 21);
printf("flag{%s}", &buf[1337]);
```

So we need to recover what is in `buf[1337]` and that should be our flag.

## GDB

We can decompress the `coredump.tar.gz` file by running
```
$ tar -xvzf coredump.tar.gz
```

Then, we can use GDB to recover what is in `buf[1337]` with the command
```
$ gdb dumpmycore coredump
```

In GDB, we can use `x/s &buf[1337]` to read a null-terminated string at the memory aaddress
`&buf[1337]`. This gives us the result
```
(gdb) x/s &buf[1337]
0x555555558579 <buf+1337>:      "my_c0r35_r_3v3rywh3r3"
```

So our flag is `flag{my_c0r35_r_3v3rywh3r3}`. woot \\(^_^)/

</details>
