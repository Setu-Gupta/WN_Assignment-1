from math import sqrt, pi, cos, sin
import numpy as np
from random import randint, seed

# Fix the seed for RNG for reproducibility
np.random.seed(0)
seed(10)

def get_QAM_points(M):
    points = []
    coords = int(sqrt(M))
    shift =  (coords - 1) / 2 
    
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

def get_PSK_points(M):
    points = []
    change = (2*pi)/M
    
    for x in range(M):
        arg = x * change
        real = cos(arg)
        imag = sin(arg)
        points.append(complex(real, imag))

    return points

def get_binary_strings(num_bits):

    strings = []
    for val in range(2**num_bits):
        bin_string = bin(val)[2:]
        prefix_length = num_bits - len(bin_string)
        bin_string = '0' * prefix_length + bin_string
        strings.append(bin_string)

    return strings

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

def awgn(symbols, variance):
    std_dev = sqrt(variance)
    n = len(symbols)
    noise = np.random.normal(loc=0, scale=std_dev, size=(n)).view(np.complex64)
    noisy_signal = symbols + noise
    return noisy_signal

def get_random_bits(length):
    bits = [randint(0, 1) for x in range(length)]
    return bits

def get_BER(Tx_bits, Rx_bits):
    total_bits = 0
    mismatches = 0
    for tx, rx in zip(Tx_bits, Rx_bits):
        total_bits += 1
        mismatches += (tx != rx)

    return (mismatches/total_bits)
