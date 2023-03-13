import numpy as np

# Simulate for 1 million bits to get an estimate the BER
NUM_BITS = 1000000

# Step size to take for search
STEP_SIZE = 0.0001
SEARCH_LIM = 10

def get_ber(thresh):
    
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
    rx_bits = np.array([1 if i > thresh else 0 for i in noisy_signal], dtype=np.uint32)

    # Get the BER
    ber = (tx_bits != rx_bits).sum() / NUM_BITS 
    return ber

def main():
    # Perform gradient descent like search for the threshold which minimizes BER
    test_point = -5/3
    while np.abs(test_point) < SEARCH_LIM:
        low_point = test_point - STEP_SIZE
        high_point = test_point + STEP_SIZE
        
        ber_low = get_ber(low_point)
        ber_test = get_ber(test_point)
        ber_high = get_ber(high_point)

        # Case 1: Positive slope
        if ber_low < ber_test <= ber_high:
            test_point -= STEP_SIZE

        # Case 2: Negative slope
        if ber_low >= ber_test > ber_high:
            test_point += STEP_SIZE

        # Case 3: Hill
        if ber_low < ber_test and ber_test > ber_high:
            if(ber_low < ber_high):
                test_point = low_point
            else:
                test_point = high_point
        
        # Case 4: Valley
        if ber_low > ber_test and ber_test < ber_high:
            print(f"The optimal threshold is {test_point} with BER of {ber_test}")
            break
        
        # Case 5: Plateau
        if ber_low == ber_test and ber_test == ber_high:
            print(f"The optimal threshold is {test_point} with BER of {ber_test}")
            break

if __name__ == "__main__":
    main()
