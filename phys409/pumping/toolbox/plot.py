import matplotlib.pyplot as plt
import datetime
import numpy as np
import seaborn
import warnings
# warnings.filterwarnings("ignore")

LINEWIDTH = 1
MARGINS = (0, 0.05)
POINT = '.'
PALETTE = 'husl'
GRID_COLOR = np.array([1, 1, 1]) * 0.85
FONT_SIZE = 13
TICK_FONT_SIZE = 13

DEFAULT_ASPECT = 'auto'
DEFAULT_GRID = False
DEFAULT_COLOR = 'k'
DEFAULT_MARKER_SIZE = 4


class Plot:
    def __init__(self):
        self.n_series = 0

    def line(self, x, y, format_=None, markersize=DEFAULT_MARKER_SIZE):
        if format_ is None:
            plt.plot(x, y, linewidth=LINEWIDTH, markersize=markersize)
        else:
            plt.plot(x, y, format_, linewidth=LINEWIDTH, markersize=markersize)
        self.n_series += 1
        return self

    def errorbar(self, x, y, y_errors, format_=None, markersize=DEFAULT_MARKER_SIZE):
        if format_ is None:
            plt.errorbar(x, y, y_errors, linewidth=LINEWIDTH, markersize=markersize)
        else:
            plt.errorbar(x, y, y_errors, fmt=format_, linewidth=LINEWIDTH, markersize=markersize)
        self.n_series += 1
        return self

    def imshow(self, data, aspect=DEFAULT_ASPECT):
        with seaborn.color_palette(PALETTE):
            plt.imshow(data, aspect=aspect, interpolation='none')
        return self

    def show(self, legend=None, xlabel=None, ylabel=None, xrange=None, yrange=None, title=None, grid=DEFAULT_GRID):
        self._format_legend(legend)
        if legend is not None:
            plt.legend(legend, fontsize=FONT_SIZE)
        if yrange is not None:
            plt.ylim(yrange)
        if xrange is not None:
            plt.xlim(xrange)
        plt.xlabel(xlabel, fontsize=FONT_SIZE)
        plt.ylabel(ylabel, fontsize=FONT_SIZE)
        plt.xticks(fontsize=TICK_FONT_SIZE)
        plt.yticks(fontsize=TICK_FONT_SIZE)
        plt.title(title)
        plt.gcf().canvas.set_window_title(_window_title())
        plt.grid(grid, color=GRID_COLOR)
        plt.margins(*MARGINS)
        plt.tight_layout()
        plt.show()

    def _format_legend(self, legend):
        if (legend is None) or (type(legend) is str):
            return None
        for i, entry in enumerate(legend):
            if entry is None:
                legend[i] = '_nolegend_'
        return legend


def _window_title():
    return f'Figure {datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}'
