#author: EnesV
import numpy as np

# Phase values defined (in radians)
phases = {
    '0000': 0, '0001': np.pi, '0010': 1.25*np.pi, '0011': 1.75*np.pi,
    '0100': 1.25*np.pi, '0101': 1.75*np.pi, '0110': 1.5*np.pi, '0111': 1.5*np.pi,
    '1000': 1.25*np.pi, '1001': 1.75*np.pi, '1010': 1.5*np.pi, '1011': 1.5*np.pi,
    '1100': 1.5*np.pi, '1101': 1.5*np.pi, '1110': 1.75*np.pi, '1111': 1.25*np.pi
}

# Checking for differences (For example: How much does the phase change when the x0 bit changes?)
for bit in range(4):
    diffs = []
    for s, p in phases.items():
        # Finding the instances where the bit is 0 and compare it to the instance where it is 1.
        if s[3-bit] == '0':
            s_flip = s[:3-bit] + '1' + s[4-bit:]
            if s_flip in phases:
                diff = (phases[s_flip] - p) % (2*np.pi)
                diffs.append(np.round(diff, 4))
    print(f"Bit x{bit} Phase changes when it changes: {set(diffs)}")


import numpy as np

# [cite_start]We are listing the 16 phase values from the PDF (from 0000 to 1111 respectively) [cite: 56-60]
phases_pi_units = np.array([
    0, 1, 1.25, 1.75, 1.25, 1.75, 1.5, 1.5,
    1.25, 1.75, 1.5, 1.5, 1.5, 1.5, 1.75, 1.25
]) * np.pi

# We are rebuilding our matrix
A = np.zeros((16, 16))
for i in range(16):
    for j in range(16):
        A[i, j] = bin(i & j).count('1') % 2

# We are using 'lstsq' (Least Squares) instead of 'solve' which gives an error.
# This method finds the best results even with singular matrices.
coeffs, residuals, rank, s = np.linalg.lstsq(A, phases_pi_units, rcond=None)

# We convert the results to T-gate units (pi/4) and clean them.
t_counts = np.round(coeffs / (np.pi/4)).astype(int)

print(" T-GATE PRESCRIPTION FOR QUESTION 11.")
for i, count in enumerate(t_counts):
    if count % 8 != 0: # We eliminate 8 and its multiples because 2pi (is the identity)
        # If the coefficient is negative or large, we adjust it to a range between 0-7.
        final_count = count % 8
        print(f"Combination {bin(i)[2:].zfill(4)} T-gate required for: {final_count}")
