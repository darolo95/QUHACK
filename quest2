from qiskit.synthesis import gridsynth_rz
import numpy as np

# Target rotation
theta = np.pi / 7
epsilon = 0.1  # Approximation error

# Approximate Rz(theta) with Clifford+T
rz_approx = gridsynth_rz(theta, epsilon=epsilon)

#  Replace S -> T T and Sdg -> Tdg Tdg in a new clean circuit
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

# Cleaned sequences
rz_clean_seq = clean_rz_sequence(rz_approx)
rz_clean_inv_seq = clean_rz_sequence(rz_approx.inverse())

# --- Print QASM 2.0 with comments ---
print('OPENQASM 2.0;')
print('include "qelib1.inc";')
print('qreg q[2];\n')

print(f'// Clifford+T decomposition for Rz(2π/7) on qubit 1')
for gate in rz_clean_seq:
    print(f'{gate} q[1]; // Rz approx')

print('\n// Controlled-Ry(2π/7) on qubits 0,1')

# Ry(theta/2) = H Rz(theta/2) H
print('// Ry(theta/2)')
print('h q[1]; // Start Ry(theta/2)')
for gate in rz_clean_seq:
    print(f'{gate} q[1];')
print('h q[1];')

# Controlled CX
print('cx q[0],q[1]; // Controlled part')

# Ry(-theta/2) = H Rz(-theta/2) H
print('// Ry(-theta/2)')
print('h q[1];')
for gate in rz_clean_inv_seq:
    print(f'{gate} q[1];')
print('h q[1];')

# Controlled CX
print('cx q[0],q[1]; // Controlled part')
