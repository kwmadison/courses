import os
from pathlib import Path

DIR = Path(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / f'{NAME}_assets'

DEFAULT_FILTER_ORDER = 2

DEFAULT_VALLEY_PROM = 0.1
DEFAULT_VALLEY_DISTANCE = 10

DEFAULT_EDGE_PROM = 0.8

