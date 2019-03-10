import numpy as np
from itertools import combinations, product, tee

seq = np.random.randint(0, 3, size = (500, 1))
print(seq)


def trans_matrix_sec_order(sequence):
    states = np.unique(sequence)
    M = np.zeros((len(states)**2, len(states)), dtype = float)
    permutations = list(product(states, repeat=2))

    def triplewise(iterable):
        a, b, c = tee(iterable, 3)
        next(b)
        next(c); next(c)
        return zip(a, b, c)


    for a, b, c in triplewise(sequence):
        prev_two = (a, b)
        M[permutations.index(prev_two)][c] += 1

    M = np.nan_to_num(np.true_divide(M, M.sum(axis = 1, keepdims= True)))

    return M

print(trans_matrix_sec_order(seq))