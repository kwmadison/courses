from toolbox.plot import Plot
from toolbox.process import *
from rb_atom import RbAtom
from data import Data
from dynamics import dynamics
from pumping_config import *
import numpy as np


def plot_energies(Bs, Rbx):
    atom = RbAtom(Rbx)
    list_energies = np.array([atom.energy_levels(B) for B in Bs]).T
    plot = Plot()
    for list_energy in list_energies:
        plot.line(Bs / GAUSS, list_energy / (C.h * C.GIGA), format_='k')
    plot.show(xlabel='B (Gauss)', ylabel='E / h (GHz)', title=f'${RB_NAMES[Rbx]}$ Energy Levels')


def plot_rf_freqs(Bs, Rbx):
    atom = RbAtom(Rbx)
    list_frequencies = np.array([atom.rf_frequencies(B) for B in Bs]).T
    plot = Plot()
    for list_frequency in list_frequencies:
        plot.line(Bs / GAUSS, list_frequency / C.MEGA, format_='k')
    plot.show(xlabel='B (Gauss)', ylabel='Frequency (GHz)', title=f'RF Transition Frequencies for ${RB_NAMES[Rbx]}$')


def plot_dynamics_Rb87(I):
    ts, Nks, Nis, As = dynamics(I)
    ts /= C.MICRO
    plot = Plot()
    for Nk in Nks:
        plot.line(ts, Nk, format_='b')
    for Ni in Nis:
        plot.line(ts, Ni, format_='r')
    plot.show(xlabel='Time (us)', ylabel='Relative Populations')

    plot = Plot()
    plot.line(ts, As)
    plot.show(xlabel='Time (us)', ylabel='Absorption (a.u.)')


def process_linear(number):
    plot = Plot()
    set_ = Data.linear.sets[number]
    time, ch1, ch2 = set_.time(), set_.ch1(), set_.ch2()
    edge1, edge2, *_ = index_edges(ch1)
    time, ch1, ch2 = time[edge1: edge2], ch1[edge1: edge2], ch2[edge1: edge2]

    # Show linear fit to current ramp
    params, errors = fit(Function.line, time, ch1, [Data.linear.ch1_bin / 2] * len(time))
    plot.points(time, ch1)
    plot.line(time, Function.line(time, *params))
    plot.show(xlabel='Time (s)', ylabel=Data.linear.ch1_label, legend=['Data Points', 'Linear Fit'])

    ch2 = denoise(ch2, 0.1)
    peak_indices = index_peaks(-ch2, distance=10, prominence=0.1)
    print(f'Peak Currents (A): {Function.line(time[peak_indices], *params)}')
    plot.line(Function.line(time, *params), ch2)
    plot.points(Function.line(time[peak_indices], *params), ch2[peak_indices])
    plot.show(xlabel=Data.linear.ch1_label, ylabel=Data.linear.ch2_label,
              title=f'Transparency - RF Frequency = {set_.rf_frequency / 1E3} kHz')


def process_trans_rf(number):
    plot = Plot()
    set_ = Data.trans_rf.sets[number]
    time, ch1, ch2 = set_.time(), set_.ch1(), set_.ch2()
    edge, *_ = index_edges(ch1)
    time, ch1, ch2 = time[edge:], ch1[edge:], ch2[edge:]

    # Show decaying sinusoidal fit to detector signal
    params, errors = fit(Function.rabi, time, ch2, [Data.trans_rf.ch2_bin / 2] * len(time))
    print(f'Decay Constant (1/s), Angular Frequency (1/s): {params[1]:.0f}, {np.abs(params[2]):.0f}')
    plot.points(time, ch2)
    plot.line(time, Function.rabi(time, *params))
    # plot.show(xlabel='Time (s)', ylabel=Data.linear.ch2_label, legend=['Data Points', 'Decaying Sin Fit'],
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
    # plot = Plot()
    # plot.line(amplitudes, freqs)
    # plot.show()
    # process_quadratic(Data.quadratic.sets[52], denoise_factor=0.1, distance=30, prominence=0.04)
    plot_dynamics_Rb87(1E3)


''' More precise valley finding
def fit_valley():
    widths = signal.peak_widths(-ydata, indices)[0]
    valleys = []
    for index, width in zip(indices, widths):
        half_range = round(width * WIDTH_TO_RANGE / 2)
        xvals = xdata[index - half_range: index + 1 + half_range]
        yvals = ydata[index - half_range: index + 1 + half_range]

        fits, cov = optimize.curve_fit(lorentzian, xvals, yvals)
        errors = np.diag(cov)
        valleys.append([fits, errors])
'''
