from math import erfc, sqrt

# Define the Q function
def q(x):
    return (1/2)*erfc(x/sqrt(2))

# Define the equation. We want to find a T such that func(T) = 0
def func(T):
    return 2*q((T-5)/2) - q(-(T+5)/2)

# Set up the bounds for binary search
start_val = -5
end_val = 5
estimate = (start_val + end_val)/2

# Set the tolerable error
err_bound = 0.001

# Perform binary search
while True:

    # Break if the value is close enough
    if(abs(func(estimate)) < err_bound):
        break

    # Perform binary search to find the estimated value of T
    if(func(estimate) > 0):
        start_val = estimate
    elif(func(estimate) < 0):
        end_val = estimate
    estimate = (start_val + end_val)/2

print(f"Estimated T = {estimate}")
