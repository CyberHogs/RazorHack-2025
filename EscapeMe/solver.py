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
# CHANGE IP
client.connect(('<DOCKER-CONTAINER-IP>', 10001))

D = {(-2, 0): b'w\n', (0, 2): b'd\n', (2, 0): b's\n', (0, -2): b'a\n'}

data, leftover = recv_frame(client)
m = [line for line in data.decode().split('\n')[1:-1] if line]
print('\n'.join(repr(line) for line in m))

P = [D[(B_r - A_r, B_c - A_c)] for (A_r, A_c), (B_r, B_c) in pairwise(bfs(m))]
 
for p in P:
    client.send(p)
    data, leftover = recv_frame(client, leftover)
    print(data.decode())
