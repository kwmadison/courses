import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import plot_config as C


class Plot:
    def __init__(self, xs, ys):
        self.ys = self._sanitize_ys(ys)
        self.n_series, self.n_points = self.ys.shape
        self.xs = self._sanitize_xs(xs)

    def line_overlay(self, options=None, legends=None, xlabel=None, ylabel=None, title=None, grid=False):
        options = self._sanitize_options(options)
        legends = self._sanitize_legends(legends)

        for x, y, option in zip(self.xs, self.ys, options):
            if option is None:
                plt.plot(x, y, linewidth=C.LINEWIDTH)
            else:
                plt.plot(x, y, option, linewidth=C.LINEWIDTH)

        if legends is not None:
            plt.legend(legends)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.gcf().canvas.set_window_title(_window_title())
        plt.grid(grid)
        plt.margins(*C.MARGINS)
        plt.show()

    def _sanitize_ys(self, ys):
        ys = np.array(ys)
        if ys.ndim == 1:
            ys = np.array([ys])
        elif ys.ndim > 2:
            raise RuntimeError(C.BAD_YS_DIMS_ERROR.format(ys.ndim))
        return ys

    def _sanitize_xs(self, xs):
        xs = np.array(xs)
        if xs.ndim == 1:
            xs = np.array([xs] * self.n_series)
        elif xs.ndim > 2:
            raise RuntimeError(C.BAD_XS_DIMS_ERROR.format(xs.ndim))
        if xs.shape != self.ys.shape:
            raise RuntimeError(C.XY_DIMS_DONT_MATCH_ERROR.format(xs.shape, self.ys.shape))
        return xs

    def _sanitize_options(self, options):
        if options is None:
            return [None] * self.n_series
        if type(options) is str:
            options = [options] * self.n_series
        elif len(options) != self.n_series:
            raise RuntimeError(C.BAD_OPTIONS_DIM_ERROR.format(self.n_series, len(options)))
        return options

    def _sanitize_legends(self, legends):
        if legends is None:
            return None
        if type(legends) is str:
            raise RuntimeError(C.BAD_LEGENDS_TYPE_ERROR.format(self.n_series))
        if len(legends) != self.n_series:
            raise RuntimeError(C.BAD_LEGENDS_DIM_ERROR.format(self.n_series, len(legends)))
        return legends


def _window_title():
    return f'Figure {datetime.now().strftime("%y-%m-%d %H:%M:%S")}'
