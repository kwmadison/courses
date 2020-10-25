from scipy import constants
import numpy as np

GAUSS = 1E-4  # Gauss B field units in Tesla
RB_NAMES = ('Rb85', 'Rb87')


class C:
    KILO = 1E3
    MEGA = 1E6
    GIGA = 1E9
    TERA = 1E12
    MILLI = 1E-3
    MICRO = 1E-6
    NANO = 1E-9

    PI = np.pi
    c = constants.c
    h = constants.h
    hbar = constants.hbar
    epsilon0 = constants.epsilon_0
    muB = constants.value('Bohr magneton')
    gS = constants.value('electron g factor')

    Rb85, Rb87 = 0, 1
