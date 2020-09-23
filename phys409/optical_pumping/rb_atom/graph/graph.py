import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import graph_config as C


FIG_DIMS = (12, 4)

class Graph:
    def __init__(self, xs, ys):
        self.ys = self._format_ys(ys)
        self.n_lines, self.n_points = self.ys.shape
        self.xs = self._format_xs(xs)

    def overlay_lines(self, options=None, legends=None, xlabel=None, ylabel=None, title=None):
        options = [options] * len(xs) if (options is None or type(options) is str) else options
        
        for x, y, option in zip(xs, ys, options):
            if option is None:
                subplot.plot(x, y)
            else:
                subplot.plot(x, y, option)

        if legends is not None:
            subplot.legend(legends)
        subplot.set_xlabel(xlabel)
        subplot.set_ylabel(ylabel)
        subplot.set_title(title)

    def _format_ys(self, ys):
        ys = np.array(ys)
        if ys.ndim == 1:
            ys = np.array([ys])
        elif ys.ndim == 2:
            pass
        else:
            raise RuntimeError(C.BAD_YS_DIMS_ERROR.format(ys.ndim))
        return ys

    def _format_xs(self, xs):
        xs = np.array(xs)
        if xs.ndim == 1:
            xs = np.array([xs] * self.n_lines)
        elif xs.ndim == 2:
            pass
        else:
            raise RuntimeError(C.BAD_XS_DIMS_ERROR.format(xs.ndim))
        if xs.shape != self.ys.shape:
            raise RuntimeError(C.XY_DIMS_DONT_MATCH_ERROR.format(xs.shape, self.ys.shape))
        return xs

    def _

def plot_stack_overlay(xs, ys, options=None, legends=None, xlabels=None, ylabels=None, subtitles=None, title=None):
    count_subplots = len(xs)
    options = [options] * count_subplots if (options is None or type(options) is str) else options
    legends = [legends] * count_subplots if legends is None else legends
    xlabels = [xlabels] * count_subplots if (xlabels is None or type(xlabels) is str) else xlabels
    ylabels = [ylabels] * count_subplots if (ylabels is None or type(ylabels) is str) else ylabels
    subtitles = [subtitles] * count_subplots if (subtitles is None or type(subtitles) is str) else subtitles

    fig = plt.figure(figsize=(FIG_DIMS[0], FIG_DIMS[1] * count_subplots), tight_layout=True)
    for i in range(len(xs)):
        subplot = fig.add_subplot(count_subplots, 1, i + 1)
        _subplot_overlay(subplot, xs[i], ys[i], options=options[i], legends=legends[i],
                         xlabel=xlabels[i], ylabel=ylabels[i], title=subtitles[i])

    fig.suptitle(title)
    plt.gcf().canvas.set_window_title(_window_title() if title is None else title)
    plt.show()


def _subplot_overlay(subplot, xs, ys, options=None, legends=None, xlabel=None, ylabel=None, title=None):
    options = [options] * len(xs) if (options is None or type(options) is str) else options

    for x, y, option in zip(xs, ys, options):
        if option is None:
            subplot.plot(x, y)
        else:
            subplot.plot(x, y, option)

    if legends is not None:
        subplot.legend(legends)
    subplot.set_xlabel(xlabel)
    subplot.set_ylabel(ylabel)
    subplot.set_title(title)


def _window_title():
    return f'Figure {datetime.now().strftime("%y-%m-%d %H:%M:%S")}'
