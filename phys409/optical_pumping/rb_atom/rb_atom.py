import numpy as np
import rb_atom_config as C


class RbAtom:
    def __init__(self, Rbx):  # Rbx = 0, 1 for Rb85, Rb87 respectively
        self.I = C.I_vals[Rbx]
        self.gI = C.gI_vals[Rbx]
        self.Ahf = C.Ahf_vals[Rbx]
        self.N = int(np.round((2 * C.S + 1) * (2 * self.I + 1)))

        mS_vals = np.arange(-C.S, C.S + 1)
        mI_vals = np.arange(-self.I, self.I + 1)
        self.basis = [(mS, mI) for mS in mS_vals for mI in mI_vals]

    def E_levels(self, B0):
        HB = C.muB * B0 * np.array([[self._HB_coeff(mS, mS_, mI, mI_)
                                     for mS, mI in self.basis] for mS_, mI_ in self.basis])
        Hhf = self.Ahf * np.array([[self._Hhf_coeff(mS, mS_, mI, mI_)
                                    for mS, mI in self.basis] for mS_, mI_ in self.basis])
        H = HB + Hhf
        E_levels = np.linalg.eigvals(H)
        return E_levels

    def _HB_coeff(self, mS, mS_, mI, mI_):
        return (C.gS * mS + self.gI * mI) * kdelta(mS, mS_) * kdelta(mI, mI_)

    def _Hhf_coeff(self, mS, mS_, mI, mI_):
        SpIm = np.sqrt((C.S - mS) * (C.S + mS + 1) * (self.I + mI) * (self.I - mI + 1)) \
               * kdelta(mS + 1, mS_) * kdelta(mI - 1, mI_)
        SmIp = np.sqrt((C.S + mS) * (C.S - mS + 1) * (self.I - mI) * (self.I + mI + 1)) \
               * kdelta(mS - 1, mS_) * kdelta(mI + 1, mI_)
        SzIz = mS * mI * kdelta(mS, mS_) * kdelta(mI, mI_)
        return (SpIm + SmIp) / 2 + SzIz


def kdelta(a, b):
    if a == b:
        return 1
    return 0
