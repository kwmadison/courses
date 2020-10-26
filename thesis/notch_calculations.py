import numpy as np
import constants as C

FREQ_CENTER = 374.74 * C.PRE.T
N_GRID = 100
RED = 'Red'
BLUE = 'Blue'
NOTCH_INFO_FORMAT = 'Notch On {} Arm\n' \
                    'Position (mm): {:.3f} to {:.3f} => {:.3f}\n' \
                    'CFG Frequency (THz): {:.3f} to {:.3f} => {:.3f}\n' \
                    'Wavelength (nm): {:.3f} to {:.3f} => {:.3f}\n' \
                    'Time (ps): {:.2f} to {:.2f} => {:.2f}'
CFG_INFO_FORMAT = '{}CFG Specifications'
BOTH_NOTCH_ERROR = 'Both arms cannot be notched at the same time. Make sure to only notch one.'


class CFG:
    # rad/ps², THz, degrees, mm⁻¹, cm, cm
    def __init__(self, freq_bandwidth, theta_incident, grating_density, grating_distance, focal_length):
        self.f0 = FREQ_CENTER
        self.fbw = freq_bandwidth
        self.thetai = np.deg2rad(theta_incident)
        self.gs = C.PRE.m / grating_density
        self.gd = grating_distance * C.PRE.c
        self.fl = focal_length * C.PRE.c

        w0 = C.c / self.f0
        self.theta0 = np.arcsin(w0 / self.gs - np.sin(self.thetai))
        self.beta = C.pi * self.gs ** 2 * self.f0 ** 3 * np.cos(self.theta0) ** 2 / (2 * self.gd * C.c)
        print(self.beta * C.PRE.p ** 2)

    def info(self):
        pass

    def notch(self, width, x0):  # mm
        x1, x2 = (x0 - width / 2) * C.PRE.m, (x0 + width / 2) * C.PRE.m
        if x1 * x2 < 0:
            raise RuntimeError(BOTH_NOTCH_ERROR)
        if abs(x2) < abs(x1):  # make sure x1 is closer to the center
            x1, x2 = x2, x1

        f1, f2 = self.pos_to_freq(x1), self.pos_to_freq(x2)
        wl1, wl2 = C.c / max(f1, f2), C.c / min(f1, f2)
        t1, t2 = 2 * C.pi * np.abs(f1 - self.f0) / self.beta, 2 * C.pi * np.abs(f2 - self.f0) / self.beta
        arm = RED if x2 < 0 else BLUE

        print(NOTCH_INFO_FORMAT.format(arm,
            min(x1, x2) / C.PRE.m, max(x1, x2) / C.PRE.m, np.abs(x2 - x1) / C.PRE.m,
            np.abs(f1 - self.f0) / C.PRE.T, np.abs(f2 - self.f0) / C.PRE.T, np.abs(f2 - f1) / C.PRE.T,
            wl1 / C.PRE.n, wl2 / C.PRE.n, np.abs(wl1 - wl2) / C.PRE.n,
            t1 / C.PRE.p, t2 / C.PRE.p, (t2 - t1) / C.PRE.p))
        return (f1 + f2) / 2

    def pos_to_freq(self, x):
        theta = np.arctan(x / self.fl) + self.theta0
        wl = (np.sin(theta) + np.sin(self.thetai)) * self.gs
        f = C.c / wl
        return f

    def freq_to_pos(self, f):
        wl = C.c / f
        theta = np.arcsin(wl / self.gs - np.sin(self.thetai))
        pos = self.fl * np.tan(theta - self.theta0)
        return pos


if __name__ == '__main__':
    sCFG = CFG(freq_bandwidth=4, theta_incident=78, grating_density=2400, grating_distance= 30, focal_length=50)
    fCFG = CFG(freq_bandwidth=20, theta_incident=44, grating_density=1500, grating_distance=30, focal_length=20)
    sCFG.notch(0.1, 5)
