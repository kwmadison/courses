import numpy as np

DEFAULT_XCOL = 0
DEFAULT_YCOL = 1
EXTENSIONS = ['txt', 'xls', 'csv', 'dat']
SEPARATORS = ['\t', '\t', ',', '\t']
FORMAT_NOT_SUPPORTED_ERROR = 'File extension .{} is not supported.'


def extract(file_path, xcol=DEFAULT_XCOL, ycol=DEFAULT_YCOL, separator=None):
    extension = file_path.split('.')[-1].lower()
    if extension in EXTENSIONS:
        with open(file_path, 'r') as file:
            raw_data = file.read()
    else:
        raise RuntimeError(FORMAT_NOT_SUPPORTED_ERROR.format(extension))
    if separator is None:
        separator = SEPARATORS[EXTENSIONS.index(extension)]

    x, y = [], []
    for row in raw_data.split('\n'):
        if row == '':
            break
        values = [_convert_float(s) for s in row.split(separator)]
        x.append(values[xcol])
        y.append(values[ycol])

    return np.array(x), np.array(y)


def _convert_float(s):
    try:
        x = float(s)
        return x
    except ValueError:
        return s
