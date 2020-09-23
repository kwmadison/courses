from graph import Graph
import numpy as np


if __name__ == '__main__':
    xs = np.random.rand(20)
    ys = np.random.rand(5, 20)

    graph = Graph(xs, ys)
    graph.line_overlay()