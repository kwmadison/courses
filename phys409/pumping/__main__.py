import plot, process
from rb_atom import RbAtom
from data import Data
from dynamics import dynamics
from pumping_config import *
import numpy as np


def plot_energies(Bs, Rbx):
    atom = RbAtom(Rbx)
    list_energies = np.array([atom.energy_levels(B) for B in Bs]).T
    p = plot.Plot()
    for list_energy in list_energies:
        p.line(Bs / GAUSS, list_energy / (C.h * C.GIGA), format_='k')
    p.show(xlabel='B (Gauss)', ylabel='E / h (GHz)', title=f'${RB_NAMES[Rbx]}$ Energy Levels')


def plot_rf_freqs(Bs, Rbx):
    atom = RbAtom(Rbx)
    list_frequencies = np.array([atom.rf_frequencies(B) for B in Bs]).T
    p = plot.Plot()
    for list_frequency in list_frequencies:
        p.line(Bs / GAUSS, list_frequency / C.MEGA, format_='k')
    p.show(xlabel='B (Gauss)', ylabel='Frequency (GHz)', title=f'RF Transition Frequencies for ${RB_NAMES[Rbx]}$')


def plot_dynamics_Rb87(I):
    ts, Nks, Nis, As = dynamics(I)
    ts /= C.MICRO
    p = plot.Plot()
    for Nk in Nks:
        p.line(ts, Nk, format_='b')
    for Ni in Nis:
        p.line(ts, Ni, format_='r')
    p.show(xlabel='Time (us)', ylabel='Relative Populations')

    p = plot.Plot()
    p.line(ts, As)
    p.show(xlabel='Time (us)', ylabel='Absorption (a.u.)')


def process_linear(number):
    p = plot.Plot()
    set_ = Data.linear.sets[number]
    time, ch1, ch2 = set_.time(), set_.ch1(), set_.ch2()
    edge1, edge2, *_ = process.index_edges(ch1)
    time, ch1, ch2 = time[edge1: edge2], ch1[edge1: edge2], ch2[edge1: edge2]

    # Show linear fit to current ramp
    params, errors = process.fit(process.Function.line, time, ch1, [Data.linear.ch1_bin / 2] * len(time))
    p.points(time, ch1)
    p.line(time, process.Function.line(time, *params))
    p.show(xlabel='Time (s)', ylabel=Data.linear.ch1_label, legend=['Data Points', 'Linear Fit'])

    ch2 = process.denoise(ch2, 0.1)
    peak_indices = process.index_peaks(-ch2, distance=10, prominence=0.1)
    print(f'Peak Currents (A): {process.Function.line(time[peak_indices], *params)}')
    p.line(process.Function.line(time, *params), ch2)
    p.points(process.Function.line(time[peak_indices], *params), ch2[peak_indices])
    p.show(xlabel=Data.linear.ch1_label, ylabel=Data.linear.ch2_label,
              title=f'Transparency - RF Frequency = {set_.rf_frequency / 1E3} kHz')


def process_trans_rf(number):
    p = plot.Plot()
    set_ = Data.trans_rf.sets[number]
    time, ch1, ch2 = set_.time(), set_.ch1(), set_.ch2()
    edge, *_ = process.index_edges(ch1)
    time, ch1, ch2 = time[edge:], ch1[edge:], ch2[edge:]

    # Show decaying sinusoidal fit to detector signal
    params, errors = process.fit(process.Function.rabi, time, ch2, [Data.trans_rf.ch2_bin / 2] * len(time))
    print(f'Decay Constant (1/s), Angular Frequency (1/s): {params[1]:.0f}, {np.abs(params[2]):.0f}')
    p.points(time, ch2)
    p.line(time, process.Function.rabi(time, *params))
    # p.show(xlabel='Time (s)', ylabel=Data.linear.ch2_label, legend=['Data Points', 'Decaying Sin Fit'],
    #           title=f'{RB_NAMES[set_.tuning]} Rabi Oscillations - RF Amplitude = {set_.rf_amplitude} V')
    return np.abs(params[5]), set_.rf_amplitude, set_.tuning


if __name__ == '__main__':
    # Bs = np.linspace(0, 0.4, 40)
    # plot_energies(Bs, C.Rb85)
    # plot_rf_freqs(Bs, C.Rb87)
    # for number in Data.linear.sets:
    #     process_linear(number)
    # freqs, amplitudes = [], []
    # for number in Data.trans_rf.sets:
    #     f, a, rbx = process_trans_rf(number)
    #     if rbx == C.Rb85:
    #         freqs.append(f)
    #         amplitudes.append(a)
    # p = plot.Plot()
    # p.line(amplitudes, freqs)
    # p.show()
    # process_quadratic(Data.quadratic.sets[52], denoise_factor=0.1, distance=30, prominence=0.04)
    plot_dynamics_Rb87(1E3)
