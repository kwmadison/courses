from scipy import constants

MEGA = 1E6
GIGA = 1E9
GAUSS = 1E-4  # Gauss B field units in Tesla

S = 1 / 2
muB = constants.value('Bohr magneton')
h = constants.value('Planck constant')
hbar = constants.value('reduced Planck constant')
gS = constants.value('electron g factor')

# (Rb85 value, Rb87 value)
Rb85, Rb87 = 0, 1
NAMES = ('{}^{85}Rb', '{}^{87}Rb')
HF_COUNT_VALS = [(5, 7), (3, 5)]
I_VALS = (5 / 2, 3 / 2)
gI_VALS = (-0.0002936400060, -0.000995141410)  # for 2S1/2 state
Ahf_VALS = (h * GIGA * 1.011910813020, h * GIGA * 3.41734130545214545)  # hyperfine constants in ground state
