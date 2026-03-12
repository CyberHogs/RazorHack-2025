def gen_asm(A, B, M, E) -> str :
    return f'''
section .text
global _start

_start:
    push rbp
    mov rbp, rsp
    sub rsp, 0x20
    
    mov rax, 0x1
    mov rdi, 0x1
    lea rsi, [rel prompt]
    mov rdx, promptsz
    syscall

    mov QWORD [rsp + 0x00], 0x0
    mov QWORD [rsp + 0x08], 0x0
    mov QWORD [rsp + 0x10], 0x0
    mov QWORD [rsp + 0x18], 0x0

    mov rax, 0x0
    mov rdi, 0x0
    mov rsi, rsp
    mov rdx, 0x20
    syscall
{ 
    ''.join(f'''
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x{i*4:02X}]
    imul rax, rax, 0x{A[i]:X}
    add  rax, 0x{B[i]:X}
    mov  r9d, 0x{M[i]:X}
    div  r9
    cmp  edx, 0x{E[i]:X}
    jne _badinput
    '''
    for i in range(8)
    )
}
    mov rax, 0x1
    mov rdi, 0x1
    lea rsi, [rel win]
    mov rdx, winsz
    syscall

    jmp _exit

_badinput:
    mov rax, 0x1
    mov rdi, 0x1
    lea rsi, [rel badinput]
    mov rdx, badinputsz
    syscall

_exit:
    add rsp, 0x20
    pop rbp
    ret

    prompt db "Enter Key: "
    promptsz equ $ -prompt

    win db "Great Job! Did you know that T. Rexes can't actually roar loudly? They can only make deep growling noises like an alligator.", 0xA
    winsz equ $ -win

    badinput db "Wrong Key!", 0xA
    badinputsz equ $ -badinput
'''

def gen_c(byte_arr, ibyte, count) -> str:
    assert len(ibyte) == len(count)
    return f'''
#include <stddef.h>
#include <stdio.h>
#include <sys/mman.h>

const unsigned char bytes[{len(byte_arr)}] = "{''.join(f"\\x{b:02X}" for b in byte_arr)}";
const unsigned char ibyte[{len(ibyte)}] = {{{','.join(f"{i}" for i in ibyte)}}};
const unsigned char count[{len(count)}] = {{{','.join(f"{n}" for n in count)}}};
int main() {{
    int size = {sum(count)};
    int prot = PROT_WRITE | PROT_EXEC;
    int flags = MAP_PRIVATE | MAP_ANON;
    int fd = -1;
    int offset = 0;

    char* addr = (char*)mmap(0, size, prot, flags, fd, offset);
    if(addr == MAP_FAILED) {{
        printf("mmap failed");
        return 0;
    }}

    int addr_off = 0;
    for(int idx = 0; idx < {len(count)}; idx++) {{
        for(int i = 0; i < count[idx]; i++) {{
            *(addr + addr_off) = bytes[ibyte[idx]]; addr_off += 1;
        }}
    }}

    ((void (*)(void))addr)();

    munmap(addr, size);
}}
'''.strip()

if __name__ == '__main__':
    from math import gcd
    from random import randint, seed
    seed(0xdeadf00d)

    flag = 'flag{3ucl1d_15_50_4w350m3_54uc3}'
    assert len(flag) == 32

    F = [sum(ord(byte) << 8*i for i, byte in enumerate(flag[i*4:(i+1)*4])) for i in range(8)] # flag as integers
    A = [0x3,      0x4,      0xB,      0xA,      0xC,      0xA,      0xB,      0x5     ] # coeff
    B = [0xD854,   0x97BB,   0x3BAE,   0x9E84,   0xD953,   0xB5F9,   0x98BD,   0x5498  ] # bias
    M = [randint(F[i] + 0xFF, 0xFFFFFFFF) for i in range(8)]

    assert len(F) == len(M) == len(A) == len(B) == 8

    E = [(A[i]*F[i] + B[i]) % M[i] for i in range(8)] 
    
    for i in range(8):
        while gcd(M[i], A[i]) != 1:
            M[i] -= 1
            E[i] = (A[i] * F[i] + B[i]) % M[i]

    print("generating nasm")
    with open("weird_software.s", "w+") as f:
        f.write(gen_asm(A, B, M, E))

    import subprocess

    print("calling nasm")
    res = subprocess.run(['nasm', '-f', 'elf64', 'weird_software.s', '-o', 'weird_software.o'])
    if res.returncode != 0:
        print("nasm failed")
        exit(res.returncode)

    print("calling objcopy")
    res = subprocess.run(['objcopy', '-O', 'binary', '-j', '.text', 'weird_software.o', 'weird_software.bin'])
    if res.returncode != 0:
        print("objcopy failed")
        exit(res.returncode)

    print("generating C code")
    from itertools import groupby
    with open('weird_software.bin', 'rb') as f:
        machine_code = f.read()
        byte_arr = list(set(machine_code))
        idx_map = {byte:idx for idx, byte in enumerate(byte_arr)}
        ibyte, count = zip(*((idx_map[k], sum(1 for _ in g)) for k, g in groupby(machine_code)))

    with open('weird_software.c', 'w+') as f:
        f.write(gen_c(byte_arr, ibyte, count))
