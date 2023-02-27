from utils import *
from math import log2
import numpy as np

class Modem:
    def __init__(self, num_bits, symbols):
       
        self.num_bits = num_bits
        self.symbols = symbols

        binary_strings = get_binary_strings(self.num_bits)

        self.mapping = {}
        self.reverse_mapping = {}
        for string, symbol in zip(binary_strings, self.symbols):
            self.mapping[string] = symbol
            self.reverse_mapping[symbol] = string

    def modulate(self, bitstream):
        
        if len(bitstream) % self.num_bits:
            prefix_size = self.num_bits - len(bitstream)
            bitstream = [0] * prefix_size + bitstream
        
        modulated_signal = []
        num_symbols = int(len(bitstream) / self.num_bits)
        for i in range(num_symbols):
            bits = bitstream[i : i+self.num_bits]
            bits_string = "".join([str(x) for x in bits])
            modulated_signal.append(self.mapping[bits_string])

        return np.asarray(modulated_signal, dtype=np.complex64)
    
    def demodulate(self, symbols):
        
        estimated_symbols = get_estimated_symbols(symbols, self.symbols)

        bit_strings = []
        for symbol in estimated_symbols:
            bit_strings.append(self.reverse_mapping[symbol])

        bits = []
        for string in bit_strings:
            for bit in string:
                bits.append(int(bit))

        return bits

class BPSK(Modem):

    def __init__(self):
        num_bits = 1
        symbols = get_PSK_points(2)
        super().__init__(num_bits, symbols)
    
    def __str__(self):
        return "BPSK"

class QPSK(Modem):

    def __init__(self):
        num_bits = 2
        symbols = get_PSK_points(4)
        super().__init__(num_bits, symbols)
    
    def __str__(self):
        return "QPSK"

class QAM_4(Modem):

    def __init__(self):
        num_bits = 2
        symbols = get_QAM_points(4)
        super().__init__(num_bits, symbols)
    
    def __str__(self):
        return "4-QAM"

class PSK_16(Modem):

    def __init__(self):
        num_bits = 4
        symbols = get_PSK_points(16)
        super().__init__(num_bits, symbols)
    
    def __str__(self):
        return "16-PSK"

class QAM_16(Modem):

    def __init__(self):
        num_bits = 4
        symbols = get_QAM_points(16)
        super().__init__(num_bits, symbols)
    
    def __str__(self):
        return "16-QAM"

class QAM_32(Modem):

    def __init__(self):
        num_bits = 5
        
        # Remove 4 corner symbols
        _symbols = get_QAM_points(36)
        max_power = 0
        for s in _symbols:
            if(max_power < np.abs(s)):
                max_power = np.abs(s)
        symbols = [s for s in _symbols if(np.abs(s) != max_power)]

        super().__init__(num_bits, symbols)

    def __str__(self):
        return "32-QAM"
