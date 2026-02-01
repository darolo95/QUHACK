#Author: EnesV
import numpy as np
from qiskit import QuantumCircuit, transpile, qasm2

def solve_challenge_6():
    # Hamiltonian: H3 = XX + ZI + IZ, Phase: pi/7
    theta = np.pi / 7
    angle = -2 * theta 
    
    qc = QuantumCircuit(2)
    
    # IZ and ZI terms (Z-rotations)
    qc.rz(angle, 0)
    qc.rz(angle, 1)
    
    # XX term (X-rotations via Basis Change)
    qc.h(0)
    qc.h(1)
    qc.cx(0, 1)
    qc.rz(angle, 1)
    qc.cx(0, 1)
    qc.h(0)
    qc.h(1)

    # Transpiling to Clifford+T basis {h, t, tdg, cx}
    basis_gates = ['h', 't', 'tdg', 'cx']
    optimized_qc = transpile(qc, basis_gates=basis_gates, optimization_level=3)
    
    # Using qasm2.dumps instead of .qasm() for Qiskit 1.0+
    print(qasm2.dumps(optimized_qc))
    return optimized_qc

solve_challenge_6()
