import numpy as np
import numpy.linalg as npla
import scipy.linalg as la
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange, CubicSpline


def vector_matrix_values():
    x = [1, 3, 2, -5]
    # print(npla.norm(x, 3))

    M = [
        [0, 3, -2, 1],
        [4, 7, -2, 3],
        [0, 6, -1, 2],
        [0, -3, -1, 3]
    ]
    # print(npla.cond(M, np.inf))


def vandermonde_interpolation(points):
    x = np.array(points[:, 0])
    y = np.array(points[:, 1])
    N = len(points)

    A = np.vander(x, increasing=True)
    c = la.solve(A, y)
    xlin = np.linspace(min(x) - 0.5, max(x) + 0.5, 101)
    ylin = sum(c[i] * xlin ** i for i in range(N))
    plt.plot(xlin, ylin, x, y, '.r')
    plt.show()


def lagrange_interpolation(points):
    x = np.array(points[:, 0])
    y = np.array(points[:, 1])
    N = len(points)

    f = lagrange(x, y)
    xlin = np.linspace(min(x) - 0.5, max(x) + 0.5, 101)
    ylin = f(xlin)
    plt.plot(xlin, ylin, x, y, '.r')
    plt.show()


def cubic_interpolation(points):
    x = np.array(points[:, 0])
    y = np.array(points[:, 1])
    # N = len(points)
    # L = [points[i+1] - points[i] for i in range(N-1)]
    # A = np.array([
    #     [L[0] ** 3, L[0] ** 2, L[0], 0, 0, 0],
    #     [3 * L[0] ** 2, 2 * L[0], 1, 0, 0, -1],
    #     [6 * L[0], 2, 0, 0, -2, 0],
    #     [0, 0, 0, L[1] ** 3, L[1] ** 2, L[1]],
    #     [0, 2, 0, 0, 0, 0],
    #     [0, 0, 0, 6 * L[1], 2, 0]
    # ])
    # b = np.array([y[1] - y[0], 0, 0, y[2] - y[1], 0, 0]).T
    # c = la.solve(A, b)
    spline = CubicSpline(x, y, bc_type='natural')
    xlin = np.linspace(min(x) - 0.5, max(x) + 0.5, 101)
    ylin = spline(xlin)
    plt.plot(xlin, ylin, x, y, '.r')
    plt.show()




if __name__ == '__main__':
    pts = np.array([  # increasing
        [1.3, 0],
        [1.5, 4],
        [2, -1],
        [2.5, 3],
        [2.8, 5],
        [3, -5]
    ])
    # vector_matrix_values()
    # vandermonde_interpolation(pts)
    lagrange_interpolation(pts)
    cubic_interpolation(pts)




