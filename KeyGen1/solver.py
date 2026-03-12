with open('data.txt', 'r') as f:
    ptr = 0x4db819 - 0x4da1b5
    len = 0xae
    concat = f.read()[ptr : ptr + len]

username = "RazorPower" + concat

from hashlib import sha256
sha256_arr = list(sha256(username.encode()).digest())

for i in range(0x20):
    sha256_arr[i] = sha256_arr[i] % 0x1a + 0x41

a = ''.join(chr(c) for c in sha256_arr[0x00:0x08]) 
b = ''.join(chr(c) for c in sha256_arr[0x08:0x10])
c = ''.join(chr(c) for c in sha256_arr[0x10:0x18])
d = ''.join(chr(c) for c in sha256_arr[0x18:0x20])

formatted = '-'.join([a, b, c, d])
print(formatted)
print(f"flag{{{formatted}}}")
