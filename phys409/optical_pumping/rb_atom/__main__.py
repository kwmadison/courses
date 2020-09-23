from rb_atom import RbAtom
import numpy as np
from graph.graph import plot_stack_overlay
import rb_atom_config as C


if __name__ == '__main__':
    atom = RbAtom(C.Rb87)
    Bs = np.linspace(0, 0.1, 10)
    E_vals = np.array([atom.E_levels(B) for B in Bs]).T

    plot_stack_overlay([Bs * C.T2G], E_vals / (C.h * C.G), xlabels='$B$ (Gauss)', ylabels='$E / h$ (GHz)',
                       title='${}^{87} Rb$ Energy Levels')
