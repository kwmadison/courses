import numpy as np
from pumping_config import C

N = 2
T = 2E-5

fik = 1 / 12 * np.array([
    [1, 1, 0, 6, 3, 1, 0, 0],
    [1, 0, 1, 0, 3, 4, 3, 0],
    [0, 1, 1, 0, 0, 1, 3, 6],
    [6, 0, 0, 4, 2, 0, 0, 0],
    [3, 3, 0, 2, 1, 3, 0, 0],
    [1, 4, 1, 0, 3, 0, 3, 0],
    [0, 3, 3, 0, 0, 3, 1, 2],
    [0, 0, 6, 0, 0, 0, 2, 4]
])

Cik = np.array([
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

tau = 27.68 * C.NANO
omega0 = 2 * C.PI * 377.10746338 * C.TERA
Pik_over_I = 6 * C.PI * C.c ** 2 / (C.hbar * omega0 ** 3) * fik @ Cik
Gik = fik / tau
n_levels = 8
