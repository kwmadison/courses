from rb_atom import RbAtom
import numpy as np
from plot import Plot
import rb_atom_config as C


if __name__ == '__main__':
    atom = RbAtom(C.Rb87)
    Bs = np.linspace(0, 0.4, 40)
    E_vals = np.array([atom.E_levels(B) for B in Bs]).T

    g = Plot(Bs / C.Gauss, E_vals / (C.h * C.G))
    g.line_overlay(options='k',
                   xlabel='B (Gauss)', ylabel='E / h (GHz)', title='${}^{85} Rb$ Energy Levels')
