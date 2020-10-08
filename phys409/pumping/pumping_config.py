import os
from pathlib import Path
from scipy import constants

DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

MEGA = 1E6
GIGA = 1E9
GAUSS = 1E-4  # Gauss B field units in Tesla
h = constants.value('Planck constant')

Rb85, Rb87 = 0, 1
RB_NAMES = ('Rb85', 'Rb87')

