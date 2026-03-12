from random import randint, choice, seed
seed(0xcafebabe)

flag = 'flag{linear_algebra_is_my_favorite!}' 

dot     = lambda A, B: sum(a * b for (a, b) in zip(A, B))
row_add = lambda A, B: [a + b for (a, b) in zip(A, B)]

# ax = b
# GOAL: given 'x', generate 'a' such that 'a' is invertible
a: list[list[int]] = []
x = [ord(c) for c in flag]
b: list[int] = []

coeff = list(range(-50,0)) + list(range(1, 50+1))
multp = list(range(-6,0))  + list(range(1, 6+1))
bias  = list(range(-15,0)) + list(range(1, 15+1))

row = [choice(coeff) for _ in range(len(x))]
a.append(row)
b.append(dot(row, x))

# Generate 'a' and 'b'
# --------------------
for i in range(1, len(x)):
    c = choice(multp)
    row = [c * r for r in a[0]]
    row[i] += choice(bias)
    a.append(row)
    b.append(dot(row, x))

# "Shuffle" 'a' and 'b'
# -------------------
for _ in range(100):
    i, j = 0, 0
    while i == j:
        i = randint(0, len(x)-1)
        j = randint(0, len(x)-1)
    a[i] = row_add(a[i], a[j])
    b[i] = b[i] + b[j]



# Solve
# -----
from numpy.linalg import solve
solve_flag = ''.join(chr(round(n)) for n in solve(a, b))
assert solve_flag == flag

print('\n'.join(', '.join(f'{n:>5}' for n in row) for row in a))
print('b')
print(', '.join(f'{n:>5}' for n in b))
print('==')
print(', '.join(f'{ord(c):>5}' for c in solve_flag))

# Generate C File
# ---------------
def generate(A: list[list[int]], x: list[int], b: list[int]) -> str:
    idx = 0
    mul = []
    add = []
    ifs = []
    def generate_row(row: list[int], b_i: int) -> tuple[list[str], list[str]]:
        nonlocal idx
        nonlocal mul
        nonlocal add
        nonlocal ifs

        row_zip = list(zip(row[::], list(range(len(x)))))
        old_idx = idx

        while row_zip:
            n = [row_zip.pop(randint(0, len(row_zip)-1) if len(row_zip) > 1 else 0) for _ in range(min(randint(2,13), len(row_zip)))]
            mul.append(f'    int _{idx} = {' + '.join(f'{r}*key[{i}]' for r, i, in n)};')
            idx += 1

        add.append(f'    int _{idx} = {'+'.join(f'_{i}' for i in range(old_idx, idx))};')
        ifs.append(f'    if(_{idx} != {b_i}) {{ goto wrong_key; }}')

        idx += 1

        return mul, ifs

    for row, b_i in zip(A, b):
        generate_row(row, b_i)

    return f'{'\n'.join(mul)}\n{'\n'.join(add)}\n{'\n'.join(ifs)}'

# print('\n'.join(''.join(row) for row in a))

# Generate C Code
username = 'RazorPower'
generated = f'''
#include "stdio.h"
#include "string.h"

int main() {{
    char usr[101];
    char key[37];

    printf("Username: ");
    fgets(usr, 101, stdin);
    // get rid of newline at the end
    size_t usr_len = strlen(usr);
    if (usr_len > 0 && usr[usr_len-1] == '\\n') {{
        usr[--usr_len] = '\\0';
    }}

    if(strcmp(usr, "{username}") != 0) {{
        printf("Wrong username!");
        return 0;
    }}

    printf("License Key: ");
    fgets(key, 37, stdin);
    // get rid of newline at the end
    size_t key_len = strlen(key);
    if (key_len > 0 && key[key_len-1] == '\\n') {{
        key[--key_len] = '\\0';
    }}

{generate(a, x, b)}

    printf("Great Job! Did you know that in 1842, the English naturalist Sir Richard Owen coined the term Dinosauria, derived from the Greek deinos, meaning \\"fearfully great,\\" and sauros, meaning \\"lizard.\\"");
    return 0;

wrong_key:
    printf("Wrong license key!");
    return 0;
}}
'''

'''
with open('awesome_software.c', 'w+') as f:
    f.write(generated[1:])
'''


