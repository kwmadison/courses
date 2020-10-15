from dynamics_config import *


def dynamics(I):
    Ni = np.zeros(n_levels)
    Nk = np.full(n_levels, 1 / n_levels)
    dt = T / N
    ts = np.linspace(0, T, N)

    Pik_ = Pik_over_I * I * dt
    Gik_ = Gik * dt

    Nks, Nis = [], []
    absorptions = []

    Gi_ = np.sum(Gik_, axis=1)
    Pi_ = np.sum(Pik_, axis=1)
    Pk_ = np.sum(Pik_, axis=0)

    print(f'Ni={Ni}')
    print(f'Nk={Nk}')
    print(f'Pik_={Pik_}')
    print(f'Pi_={Pi_}')
    print(f'Pk_={Pk_}')
    print(f'Gik_={Gik_}')


    for _ in ts:
        Nis.append(Ni)
        Nks.append(Nk)
        absorptions.append(np.dot(Pk_, Nk))

        rNk = Ni @ Pik_ - np.multiply(Pk_, Nk) + Ni @ Gik_
        rNi = Nk @ Pik_.T - np.multiply(Pi_, Ni) - np.multiply(Gi_, Ni)
        Nk += dt * rNk
        Ni += dt * rNi

    return ts, np.array(Nks).T, np.array(Nis).T, absorptions


