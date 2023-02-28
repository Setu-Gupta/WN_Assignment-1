from utils import *

NUM_SIGNALS = 1000000

# Create the modulator
symbols = get_64QAM_points()
binary_strings = get_binary_strings()
mapping, rev_mapping = get_mapping(binary_strings, symbols)

# Generate a random signal stream
tx_signals = get_random_signals(NUM_SIGNALS)

# Modulate the signals
modulated_signals = modulate(mapping, tx_signals)

# Pass the signal through a AWGN channel
variance = 0.1  # 0.1 is equivalent to -10dB
noisy_signals = awgn(modulated_signals, variance)

for x, y in zip(modulated_signals, noisy_signals):
    print(x, y)

# Demodulate the noisy signals
rx_signals = demodulate(noisy_signals, symbols, rev_mapping)

# Compute the SER
ser = get_SER(tx_signals, rx_signals)
print(f"SER is {ser}")
