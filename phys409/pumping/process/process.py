import scipy.optimize as optimize
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from process_config import *


def denoise(y, factor, order=DEFAULT_FILTER_ORDER):
    params = signal.butter(order, factor, btype='lowpass')
    y = signal.filtfilt(*params, y)
    return y


def index_valleys(y, distance=DEFAULT_VALLEY_DISTANCE, prominence=DEFAULT_VALLEY_PROM):
    prominence *= span(y)
    indices, _ = signal.find_peaks(-y, distance=distance, prominence=(prominence, None))
    return indices


def index_edges(y, prominence=DEFAULT_EDGE_PROM):
    prominence *= span(y)
    indices = np.where(abs(y[:-1] - y[1:]) >= prominence)[0] + 1
    return indices


def span(y):
    return np.max(y) - np.min(y)


def fit(f, x, y, sigma):
    params, cov = optimize.curve_fit(f, x, y, sigma=sigma, absolute_sigma=True)
    errors = np.diag(cov)
    return params, errors


class Function:
    @staticmethod
    def line(x, a, b):
        return a * x + b

    @staticmethod
    def rabi_oscillation(x, a1, a2, omega, phi, A, B, y0):
        return A * np.exp(-a1 * x) + B * np.exp(-a2 * x) * np.cos(omega * x + phi) + y0


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


def gaussian_valley(x, x0, y0, h, sigma):  # tried and failed
    return -h * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + y0


def polynomial(x, x0, y0, a, b):  # tried and failed
    return a * (x - x0) ** 2 + b * (x - x0) + y0


def lorentzian(x, x0, y0, A, w):  # central one worked, others failed
    return A * w ** 2 / ((x - x0) ** 2 + w ** 2) + y0
'''
