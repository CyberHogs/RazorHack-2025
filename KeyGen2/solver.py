import re
import numpy as np

# parse figures 2, 3, and 4.
with open('src.txt', 'r') as f:
    src = f.read()

mul, add, eq = src.split('\n\n')

mul = dict(line[4:-1].split(' = ') for line in mul.splitlines())

add = dict(line[4:-1].split(' = ') for line in add.splitlines())
add = dict(
    (var_a, ' + '.join(mul[var_m] for var_m in add[var_a].split('+')))
    for var_a in add
)

eq = dict(line[3:-21].split(' != ') for line in eq.splitlines())
eq = dict((var_e, int(eq[var_e])) for var_e in eq)

add = dict(
    (var_a, dict(
        (int(re.search(r'\d+', key_idx).group(0)), int(const))
        for term in add[var_a].split(' + ')
        for const, key_idx in [term.split('*')]
    ))
    for var_a in add
)

# Create the 36x36 matrix and the length-36 vector. It's fine to create these separately in two
# different iterations because dictionaries are guaranteed to be ordered when iterating over them.
A = [[add[var_a][idx] for idx in range(36)] for var_a in add]
b = [eq[var_a] for var_a in add]

# solve for `key`
k = ''.join(chr(round(n)) for n in np.linalg.solve(A, b))
print(k)
