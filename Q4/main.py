import numpy as np

# Simulate for 1 million bits to get an estimate the BER
NUM_BITS = 1000000

# Set the threshold
THRESH = -5 + 10/3

def main():
    
    # Generate a sequence of random bits
    tx_bits = np.random.choice([0, 1], size=NUM_BITS, p=[1/3, 2/3]) 
   
    # Modulate the bits to get the signal
    signal = np.array([5 if i == 1 else -5 for i in tx_bits], dtype=np.float32)

    # Generate the gaussian noise
    std_dev = 2 # Since variance is 4, the standard deviation will be sqrt(4) = 2
    noise = np.random.normal(loc=0, scale=std_dev, size=(NUM_BITS))

    # Apply the gaussian noise
    noisy_signal = signal + noise

    # Demodulate the signal
    rx_bits = np.array([1 if i > THRESH else 0 for i in noisy_signal], dtype=np.uint32)

    # Get the BER
    ber = (tx_bits != rx_bits).sum() / NUM_BITS 
    print(f"Got bit error rate of {ber}")

if __name__ == "__main__":
    main()
