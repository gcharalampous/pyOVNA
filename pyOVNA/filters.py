import numpy as np

def filter_data(frequencies, powers, min_frequency, max_frequency):
    mask = (frequencies >= min_frequency) & (frequencies <= max_frequency)
    return frequencies[mask], powers[mask]

def supergf(f, fcenter, width, order):
    return np.exp(-((f - fcenter) / width) ** order)

def rectf(f, fcenter, width):
    return np.abs(f - fcenter) < width
