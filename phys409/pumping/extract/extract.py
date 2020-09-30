from scipy.signal import butter, filtfilt
import numpy as np


def extract(file_path, x_col=1, y_col=2, start_row=1, trim_zeros=True, separator='\t'):
    extension = file_path.split('.')[-1]

    if extension in ['txt', 'xls', 'csv']:
        with open(f'toolbox_assets/{file_path}', 'r') as file:
            raw_data = file.read()
    else:
        raise RuntimeError(f'File extension .{extension} is not supported.')

    if extension == 'csv':
        separator = ','

    data = []
    for row in raw_data.split('\n'):
        values = row.split(separator)
        try:
            values = [float(v) for v in values]
        except ValueError:
            start_row -= 1
            continue
        data += [values]

    row_count, col_count = np.shape(data)
    start_row = max(1, start_row)

    if start_row > row_count:
        raise RuntimeError(f'Start row {start_row} exceeds number of rows {row_count}.')
    if x_col > col_count:
        raise RuntimeError(f'x column {x_col} exceeds number of columns {col_count}.')
    if y_col > col_count:
        raise RuntimeError(f'y column {y_col} exceeds number of columns {col_count}.')

    data = np.transpose(np.array(data)[start_row - 1:])
    x, y = data[x_col - 1], data[y_col - 1]

    if trim_zeros:
        start_index, end_index = 0, row_count - start_row
        while y[start_index] == 0:
            start_index += 1
        while y[end_index] == 0:
            end_index -= 1
        x, y = x[start_index: end_index + 1], y[start_index: end_index + 1]

    return x, y


def denoise(values, factor):
    params = butter(2, factor, btype='low', analog=False)
    values = filtfilt(*params, values)
    return values
