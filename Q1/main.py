from modems import BPSK, QPSK, QAM_4, PSK_16, QAM_16, QAM_32
from utils import get_random_bits, awgn, get_BER 
from matplotlib import pyplot as plt
import sys
from joblib import Parallel, delayed
from multiprocessing import cpu_count

# Set the simulation cycles and plots directory
plot_dir = "./plots/"
sim_cycles = 10000

def compute_BER(modem, noise):
    # Generate a 12 kilobit long binary string
    tx_bits = get_random_bits(12000)

    # Modulate the signal
    symbols = modem.modulate(tx_bits)

    # Pass the signal through a AWGN channel
    noisy_symbols = awgn(symbols, noise)

    # Demodulate the signal
    rx_bits = modem.demodulate(noisy_symbols)

    # Compute the BER
    return get_BER(tx_bits, rx_bits)

def plot_BER(modem):
    # Store the SNR values in an array in dB
    snr_db = [0, -10, -20, -30, -40, -50, -60]

    # Store the noise values for all SNR values (assuming that the signal power is unity)
    noise_linear = [1/(10**(snr/10)) for snr in snr_db]

    futures = []
    bers = []
    for noise in noise_linear:
        # Start the BER computation in parallel
        ber = sum(Parallel(n_jobs=cpu_count())(delayed(compute_BER)(modem, noise) for _ in range(sim_cycles)))
        ber /= sim_cycles
        bers.append(ber)

    # Plot the graph of BER v/s SNR
    xlabels = [str(s) + 'dB' for s in snr_db]
    xticks = [x for x in range(len(snr_db))]
    plot_name = plot_dir + str(modem) + ".png"
    plt.figure()
    plt.plot(bers, marker='o', linestyle='dashed')
    plt.xticks(xticks, labels=xlabels)
    plt.xlabel("SNR values in dB")
    plt.ylabel("Bit Error Rate")
    plt.title("BER v/s SNR for " + str(modem))
    plt.gca().autoscale(enable=True, axis='x', tight=True)
    plt.savefig(plot_name)

def print_usage():
    print("Specify the modulator to be used as the first and only argument")
    print("The following modulators are supported:")
    print("\tBPSK")
    print("\tQPSK")
    print("\t4-QAM")
    print("\t16-PSK")
    print("\t16-QAM")
    print("\t32-QAM")
    exit(-1)

def main():
    
    if  len(sys.argv) < 2:
        print_usage()
    modem_type = sys.argv[1].strip()
    
    modem = None
    if modem_type == "BPSK":
        modem = BPSK()
    elif modem_type == "QPSK":
        modem = QPSK()
    elif modem_type == "4-QAM":
        modem = QAM_4()
    elif modem_type == "16-PSK":
        modem = PSK_16()
    elif modem_type == "16-QAM":
        modem = QAM_16()
    elif modem_type == "32-QAM":
        modem = QAM_32()
    
    plot_BER(modem)

if __name__ == "__main__":
    main()
