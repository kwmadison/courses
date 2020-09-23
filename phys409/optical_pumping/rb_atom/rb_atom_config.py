from scipy import constants

M = 1E6
G = 1E9
T2G = 1E4

S = 1 / 2
muB = constants.value('Bohr magneton')
h = constants.value('Planck constant')
hbar = constants.value('reduced Planck constant')
gS = constants.value('electron g factor')

# (Rb85 value, Rb87 value)
Rb85, Rb87 = 0, 1
I_vals = (5 / 2, 3 / 2)
gI_vals = (-0.0002936400060, -0.000995141410)
# todo: which constant do I use? 2S1/2 or 2P1/2?
Ahf_vals = (h * G * 1.011910813020, h * G * 3.41734130545214545)  # hyperfine interaction constants in ground state