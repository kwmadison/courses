from dynamics_config import *
import pandas


def dynamics(I):
    Nk = np.full(K_LEVELS, 1 / K_LEVELS)
    Ni = np.zeros(I_LEVELS)
    dt = T / N
    ts = np.linspace(0, T, N + 1)

    Pik, Gik = PIK_OVER_I * I * dt, GIK * dt
    Gi = np.sum(Gik, axis=1)
    Pi = np.sum(Pik, axis=1)
    Pk = np.sum(Pik, axis=0)
    Nks, Nis, absorptions = [], [], []

    for _ in ts:
        Nks.append(Nk)
        Nis.append(Ni)
        absorptions.append(np.dot(Pk, Nk) / dt)

        # rk = Ni @ Pik - np.multiply(Pk, Nk) + Ni @ Gik
        # ri = Nk @ Pik.T - np.multiply(Pi, Ni) - np.multiply(Gi, Ni)
        # print(pandas.DataFrame(Ni @ Pik))
        # print(pandas.DataFrame(np.multiply(Pk, Nk)))
        # print(pandas.DataFrame(Ni @ Gik))
        Nk += Ni @ Pik - np.multiply(Pk, Nk) + Ni @ Gik
        Ni += Nk @ Pik.T - np.multiply(Pi, Ni) - np.multiply(Gi, Ni)

    return ts, np.array(Nks).T, np.array(Nis).T, absorptions

