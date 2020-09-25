from plot import Plot
import numpy as np

if __name__ == '__main__':
    xs = np.arange(1, 21)
    ys = np.random.rand(3, 20)

    plot = Plot(xs, ys)
    plot.line_overlay(options='k', legends=['One', 'Two', 'Three'],
                      xlabel='Trial Number', ylabel='Measured Values', title='Plot Title Here', grid=True)
