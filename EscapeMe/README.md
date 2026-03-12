# EscapeMe
Created by Tyr Rex.

To test locally:
- Run `docker compose up` in the directory to start the server.
- Then find the ip of the container with `docker inspect -f "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}" escape-me`
- Then connect to the server with `nc 

or use `ncat`:
```
# start the server
ncat -l -k -v -p 10001 -e ./EscapeMe

# connect to the server
ncat localhost 10001
```

<details>
    <summary>Flag</summary>
    <code>flag{w7f_15_br34d7h_f1r57_534rch}</code>
</details>

## Files Provided
- None

## Tools
- Python

## Steps to Solve

<details>
<summary>Steps to Solve</summary>

Connecting to the server, we are greeted with a maze that tells us we can move around using WASD and
that we must reach the `X`. We also only have a limited amount of time. The maze is too big to solve
in time by hand, but we can create a script that connects to the server and solves the maze.

```py
import socket
from itertools import pairwise

def bfs(m):
    p = (1, 1)
    Q = [(p,)]
    V = set()

    for i in range(len(m)):
        assert len(m[i]) == len(m[0])
    W = len(m[0]) - 1
    H = len(m)    - 1

    while Q:
        P = Q.pop(0)
        N_r, N_c = P[-1]
        for D_r, D_c in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            E_r, E_c = N_r + D_r, N_c + D_c

            if not (0 <= E_r <= H) or not (0 <= E_c <= W):
                continue

            if m[E_r][E_c] != ' ':
                continue

            E_r, E_c = N_r + 2*D_r, N_c + 2*D_c
            if (E_r, E_c) in V:
                continue

            if m[E_r][E_c] == 'X':
                return (*P, (E_r, E_c))

            V.add((E_r, E_c))
            Q.append((*P, (E_r, E_c)))

def recv_frame(c: socket.socket, leftover: bytes = b''):
    buf = leftover
    while True:
        data = c.recv(2**10)
        if b'Move: ' in data:
            idx = data.find(b'Move: ') + 6
            buf += data[:idx]
            data = data[idx:]
            return buf, data

        if not data:
            return buf, b''

        buf += data

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.17.0.2', 9001))

D = {(-2, 0): b'w\n', (0, 2): b'd\n', (2, 0): b's\n', (0, -2): b'a\n'}

data, leftover = recv_frame(client)
m = [line for line in data.decode().split('\r\n')[1:-1] if line]
print('\n'.join(repr(line) for line in m))

P = [D[(B_r - A_r, B_c - A_c)] for (A_r, A_c), (B_r, B_c) in pairwise(bfs(m))]
 
for p in P:
    client.send(p)
    data, leftover = recv_frame(client, leftover)
    print(data.decode())
```

The code is a little terse to read but tl;dr:
- `bfs(m)` returns a tuple of coordinates of the path to the `X`
- `recv_frame` is to make sure that when we do `client.recv`, we're getting all of the 
- we then connect to the server using `client.connect(('localhost', 1337))`
- `m` is the maze that the server sends immediately
- `P` is the keys needed to move the player around to reach `x`
- the for-loop sends each key in `P` to the server. we need to do `recv_frame` each time so that
when it solves the maze, we actually see the flag sent from the server.

Running the script we get `flag{w7f_15_br34d7h_f1r57_534rch}`
</details>
