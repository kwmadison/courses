import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from plot_config import *


class Plot:
    def __init__(self):
        self.n_series = 0

    def line(self, x, y, format_=None):
        x, y = self._sanitize_xy(x, y)
        if format_ is None:
            plt.plot(x, y, linewidth=LINEWIDTH, markersize=MARKERSIZE)
        else:
            plt.plot(x, y, format_, linewidth=LINEWIDTH, markersize=MARKERSIZE)
        self.n_series += 1

    def points(self, x, y, format_=None):
        format_ = '.' if format_ is None else format_
        self.line(x, y, format_=format_)

    def show(self, legend=None, xlabel=None, ylabel=None, title=None, grid=DEFAULT_GRID):
        legend = self._sanitize_legend(legend)
        if legend is not None:
            plt.legend(legend)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.gcf().canvas.set_window_title(_window_title())
        plt.grid(grid)
        plt.margins(*MARGINS)
        plt.tight_layout()
        plt.show()

    def _sanitize_xy(self, x, y):
        x, y = np.array(x), np.array(y)
        if y.ndim > 1:
            raise RuntimeError(BAD_Y_DIMS_ERROR.format(y.ndim))
        if x.ndim > 1:
            raise RuntimeError(BAD_X_DIMS_ERROR.format(x.ndim))
        if x.shape != y.shape:
            raise RuntimeError(XY_DIMS_DONT_MATCH_ERROR.format(x.shape, y.shape))
        return x, y

    def _sanitize_legend(self, legend):
        if legend is None:
            return None
        if type(legend) is str:
            legend = np.array(legend)
        if len(legend) != self.n_series:
            raise RuntimeError(BAD_LEGEND_DIM_ERROR.format(self.n_series, len(legend)))
        return legend


def _window_title():
    return f'Figure {datetime.now().strftime("%y-%m-%d %H:%M:%S")}'
