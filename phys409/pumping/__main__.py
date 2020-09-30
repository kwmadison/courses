from rb_atom import RbAtom
import numpy as np
from plot import Plot
from rb_atom_config import *


def plot_energies(B, Rbx):
    atom = RbAtom(Rbx)
    E_vals = np.array([atom.E_levels(B) for B in B]).T
    g = Plot(B / GAUSS, E_vals / (h * GIGA))
    g.line_overlay(options='k', xlabel='B (Gauss)', ylabel='E / h (GHz)', title=f'${NAMES[Rbx]}$ Energy Levels')


def plot_rf_freqs(B, Rbx):
    atom = RbAtom(Rbx)
    f_vals = np.array([atom.RF_frequencies(B) for B in B]).T
    g = Plot(B / GAUSS, f_vals / MEGA)
    g.line_overlay(options='k', xlabel='B (Gauss)', ylabel='Frequency (GHz)',
                   title=f'RF Transition Frequencies for ${NAMES[Rbx]}$')


if __name__ == '__main__':
    Bs = np.linspace(0, 0.4, 40)
    plot_energies(Bs, Rb85)
