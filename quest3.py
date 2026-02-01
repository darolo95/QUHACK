# quest3_rz_cnot_sandwich.py
from qiskit.synthesis import gridsynth_rz
import numpy as np

# --- Parameters ---
theta = 2 * np.pi / 7
epsilon = 0.1  # Approximation error

# --- Approximate Rz(theta) with Clifford+T ---
rz_approx = gridsynth_rz(theta, epsilon=epsilon)

# --- Convert S/SDG into T/Tdg sequences ---
def clean_rz_sequence(rz_circ):
    seq = []
    for instr in rz_circ.data:
        gate = instr.operation.name
        if gate == 's':
            seq.extend(['t', 't'])
        elif gate == 'sdg':
            seq.extend(['tdg', 'tdg'])
        else:
            seq.append(gate)  # H, T, Tdg, X
    return seq

rz_clean_seq = clean_rz_sequence(rz_approx)

# --- Print QASM 2.0 ---
print('OPENQASM 2.0;')
print('include "qelib1.inc";')
print('qreg q[2];\n')

# Sandwich: (I ⊗ CNOT) * (I ⊗ Rz) * (I ⊗ CNOT)
print('// --- (I ⊗ CNOT) * Rz(2π/7) * (I ⊗ CNOT) ---\n')

# First I⊗CNOT
print('cx q[0],q[1]; // First CNOT\n')

# I⊗Rz(2pi/7)
print('// Apply Rz(2π/7) on qubit 1')
for gate in rz_clean_seq:
    print(f'{gate} q[1];')

# Second I⊗CNOT
print('\ncx q[0],q[1]; // Second CNOT')
