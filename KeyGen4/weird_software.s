
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

    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x00]
    imul rax, rax, 0x3
    add  rax, 0xD854
    mov  r9d, 0x706F448E
    div  r9
    cmp  edx, 0x5546946A
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x04]
    imul rax, rax, 0x4
    add  rax, 0x97BB
    mov  r9d, 0x8DD910CF
    div  r9
    cmp  edx, 0x72234409
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x08]
    imul rax, rax, 0xB
    add  rax, 0x3BAE
    mov  r9d, 0xA5B027C4
    div  r9
    cmp  edx, 0x372D6CBA
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x0C]
    imul rax, rax, 0xA
    add  rax, 0x9E84
    mov  r9d, 0x90FF6F99
    div  r9
    cmp  edx, 0x62BA63A3
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x10]
    imul rax, rax, 0xC
    add  rax, 0xD953
    mov  r9d, 0xB6343131
    div  r9
    cmp  edx, 0x9B07F73C
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x14]
    imul rax, rax, 0xA
    add  rax, 0xB5F9
    mov  r9d, 0xDF9FF3E3
    div  r9
    cmp  edx, 0xC562FA6B
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x18]
    imul rax, rax, 0xB
    add  rax, 0x98BD
    mov  r9d, 0xD98BCC54
    div  r9
    cmp  edx, 0x8B341746
    jne _badinput
    
    xor  rdx, rdx
    mov  eax, DWORD [rsp + 0x1C]
    imul rax, rax, 0x5
    add  rax, 0x5498
    mov  r9d, 0xDE8215FB
    div  r9
    cmp  edx, 0xB4FD19EB
    jne _badinput
    
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
