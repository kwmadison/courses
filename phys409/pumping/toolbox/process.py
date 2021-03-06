import scipy.optimize as optimize
import scipy.signal as signal
import numpy as np

DEFAULT_FILTER_ORDER = 2
DEFAULT_VALLEY_PROM = 0.1
DEFAULT_VALLEY_DISTANCE = 10
DEFAULT_EDGE_PROM = 0.8
DEFAULT_MAXFEV = 10000
DEFAULT_BINS = 20
DEFAULT_RELATIVE_STEP = 1E-8
DEFAULT_ABSOLUTE_STEP = 1E-8


def hist2d(x, y, bins=DEFAULT_BINS):
    return np.histogram2d(x, y, bins=bins)


def trim_zeros(x):
    start, end = 0, len(x)
    while x[start] == 0:
        start += 1
    while x[end] == 0:
        end -= 1
    return x[start: end + 1]


def denoise(y, factor, order=DEFAULT_FILTER_ORDER):
    params = signal.butter(order, factor, btype='lowpass')
    y = signal.filtfilt(*params, y)
    return y


def index_peaks(y, distance=DEFAULT_VALLEY_DISTANCE, prominence=DEFAULT_VALLEY_PROM):
    prominence *= np.max(y) - np.min(y)
    indices, _ = signal.find_peaks(y, distance=distance, prominence=(prominence, None))
    return indices


def index_edges(y, prominence=DEFAULT_EDGE_PROM):
    prominence *= np.max(y) - np.min(y)
    indices = np.where(abs(y[:-1] - y[1:]) >= prominence)[0] + 1
    return indices


def fit(f, x, y, sigma, absolute_sigma=True):
    params, cov = optimize.curve_fit(f, x, y, sigma=sigma, absolute_sigma=absolute_sigma, maxfev=DEFAULT_MAXFEV)
    errors = np.diag(cov)
    return params, errors


def fit_func(f, x, y, sigma, absolute_sigma=True, relative_step=DEFAULT_RELATIVE_STEP, absolute_step=DEFAULT_ABSOLUTE_STEP):
    params, errors = fit(f, x, y, sigma, absolute_sigma=absolute_sigma)

    def func(x_vals, sigma=None):
        x_vals = np.array(x_vals)
        y_errors = np.zeros_like(x_vals)
        for i, (param, error) in enumerate(zip(params, errors)):
            aparams, bparams = params.copy(), params.copy()
            dparam = np.maximum(np.abs(param * relative_step), absolute_step)
            aparams[i] += dparam
            bparams[i] -= dparam
            diff = np.divide(f(x_vals, *aparams) - f(x_vals, *bparams), 2 * dparam)
            y_errors = np.add(y_errors, np.power(diff * error, 2))
        if sigma is not None:
            dx = np.maximum(np.abs(x_vals * relative_step), absolute_step)
            ax = x_vals + dx
            bx = x_vals - dx
            diff = np.divide(f(ax, *params) - f(bx, *params), 2 * dx)
            y_errors = np.add(y_errors, np.power(np.multiply(diff, sigma), 2))
        return f(x_vals, *params), np.sqrt(y_errors)

    return func


class Function:
    @staticmethod
    def line(x, a, b):
        x = np.array(x)
        return a * x + b

    @staticmethod
    def rabi(x, A, a1, B, a2, omega, phi, y0):
        x = np.array(x)
        return A * np.exp(-a1 * x) + B * np.exp(-a2 * x) * np.cos(omega * x + phi) + y0

    @staticmethod
    def lorentzian(x, A, w, x0, y0):
        x = np.array(x)
        return A * w ** 2 / ((x - x0) ** 2 + w ** 2) + y0

    @staticmethod
    def gaussian(x, h, x0, sigma, y0):
        x = np.array(x)
        return h / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + y0

    @staticmethod
    def decay(x, A, a, y0):
        x = np.array(x)
        return A * np.exp(-a * x) + y0

