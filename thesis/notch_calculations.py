from scipy import constants
import numpy as np

C = constants.c
PI = constants.pi
PICO = 1E-12
NANO = 1E-9
MILLI = 1E-3
CENTI = 1E-2
TERA = 1E12

FREQ_CENTER = 375 * TERA
N_GRID = 100
NOTCH_INFO_FORMAT = 'Notch: frequency={:.3f}THz, wavelength={:.3f}nm, time={:.2f}ps'


class CFG:
    # units: rad/ps², THz, degrees, mm⁻¹, cm
    def __init__(self, chirp_rate, freq_bandwidth, theta_incident, grating_density, focal_length):
        self.f0 = FREQ_CENTER
        self.beta = chirp_rate / (2 * PI) / PICO ** 2
        self.fbw = freq_bandwidth
        self.thetai = np.deg2rad(theta_incident)
        self.gd = MILLI / grating_density
        self.fl = focal_length * CENTI

        w0 = C / self.f0
        self.theta0 = np.arcsin(w0 / self.gd - np.sin(self.thetai))

    def notch(self, width, pos):
        f1 = self.pos_to_freq(pos - width / 2)
        f2 = self.pos_to_freq(pos + width / 2)
        df = np.abs(f2 - f1)
        dwl = np.abs(C / f1 - C / f2)
        dt = df / self.beta
        print(NOTCH_INFO_FORMAT.format(df / TERA, dwl / NANO, dt / PICO))

    def pos_to_freq(self, pos):
        theta = np.arctan(pos / self.fl) + self.theta0
        wl = (np.sin(theta) + np.sin(self.thetai)) * self.gd
        f = C / wl
        return f

    def freq_to_pos(self, f):
        wl = C / f
        theta = np.arcsin(wl / self.gd - np.sin(self.thetai))
        pos = self.fl * np.tan(theta - self.theta0)
        return pos


if __name__ == '__main__':
    sCFG = CFG(chirp_rate=0.017, freq_bandwidth=4, theta_incident=70, grating_density=2400, focal_length=50)
    fCFG = CFG(chirp_rate=0.3, freq_bandwidth=20, theta_incident=30, grating_density=1500, focal_length=20)
    sCFG.notch(1E-4, 0)
