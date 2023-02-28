import numpy as np
from random import randint, seed
from math import sqrt

# Fix the seed for RNG for reproducibility
np.random.seed(0)
seed(10)

# Generate points in the constellation of 64-QAM
def get_64QAM_points():
    points = []
    coords = 8
    shift =  7 / 2 
    
    for x in range(coords):
        for y in range(coords):
            points.append(complex(x - shift, y - shift))
    
    max_power = 0
    for p in points:
        if(max_power < np.abs(p)):
            max_power = np.abs(p)

    scale_factor = 1/max_power
    scaled_points = np.array([x * scale_factor for x in points])

    return scaled_points

# Get all the binary strings which represent each of the symbols in the constellation
def get_binary_strings():
    _strings = [bin(value)[2:] for value in range(64)]
    
    strings = []
    for s in _strings:
        prefix_length = 6 - len(s)
        new_s = '0' * prefix_length + s
        strings.append(new_s)

    return strings

# Get the mapping between the binary strings and symbols
def get_mapping(strings, symbols):
    mapping = {}
    rev_mapping = {}
    for bin_str, sym in zip(strings, symbols):
        mapping[bin_str] = sym
        rev_mapping[sym] = bin_str

    return mapping, rev_mapping

# Generate random signals
def get_random_signals(num):
    # 64-QAM means that each symbol represents 6 bits. Therefore create 6 bit strings
    random_values = ["".join([str(randint(0,1)) for bit in range(6)]) for value in range(num)]
    return random_values

# Modulate the binary strings
def modulate(mapping, strings):
    mod = []
    for string in strings:
        mod.append(mapping[string])
    return mod

# Add AWGN noise with zero mean and unit variance
def awgn(symbols, variance):
    n = len(symbols)
    std_dev = sqrt(variance)
    noise = np.random.normal(loc=0, scale=std_dev, size=(n)).view(np.complex64)
    noisy_signal = symbols + noise
    return noisy_signal

# Get the nearest symbol
def get_estimated_symbols(recv_symbols, symbols_set):
    estimated_symbols = []
    for rs in recv_symbols:
        min_dist = np.Inf
        estimate = symbols_set[0]
        for s in symbols_set:
            if(np.abs(rs - s) < min_dist):
                min_dist = np.abs(rs - s)
                estimate = s
        estimated_symbols.append(estimate)
    return estimated_symbols

# Demodulate the received signal
def demodulate(recv_symbols, symbols_set, rev_mapping):
    strings = []
    estimated_symbols = get_estimated_symbols(recv_symbols, symbols_set)
    for es in estimated_symbols:
        strings.append(rev_mapping[es])
    return strings

# Get the symbol error rate
def get_SER(Tx_signals, Rx_signals):
    total_signals = 0
    mismatches = 0
    for tx, rx in zip(Tx_signals, Rx_signals):
        total_signals += 1
        mismatches += (tx != rx)

    return (mismatches/total_signals)
