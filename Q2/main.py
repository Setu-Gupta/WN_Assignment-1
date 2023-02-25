import numpy as np
import sys
from matplotlib import pyplot as plt

# Set the signal frequency
base_frequency = 2 * np.pi * 1.5e9

def print_usage():
    print("The first argument is the phase deviation factor in radians")
    print("The second argument is the attenuation factor")
    print("The third argument is the number of sinusoids")
    exit(-1)

def main():
    if len(sys.argv) < 4:
        print_usage()

    theta = float(sys.argv[1])
    alpha = float(sys.argv[2])
    num = int(sys.argv[3])

    # Generate the timesteps for plotting
    time = np.linspace(0, 1e-8, 1000000)

    # Generate the pure signal
    pure_signal = np.sin(base_frequency * time)

    # Compute the noisy signal
    noisy_signal = np.zeros(pure_signal.shape)
    for i in range(num):
        amplitude = 1 / ((i + 1) * alpha)
        phase = theta * (i + 1)
        noise = amplitude * np.sin((base_frequency * time) + phase)
        noisy_signal += noise
    
    # Compute the SNR
    snr = np.zeros(pure_signal.shape)
    for idx, signals in enumerate(zip(pure_signal, noisy_signal)):
        s, ns = signals
        snr[idx] = np.abs(s/(ns - s))

    plt.figure()
    plt.xlabel("Time steps")
    plt.ylabel("SNR")
    plt.title("SNR v/s time")
    plt.plot(snr)
    plt.gca().autoscale(enable=True, axis='x', tight=True)
    plt.savefig(str(num) + ".png")

if __name__ == "__main__":
    main()
