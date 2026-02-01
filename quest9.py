#author: EnesV
import numpy as np
from qiskit import QuantumCircuit, transpile, qasm2
from qiskit.quantum_info import Operator

def solve_challenge_9():
    print("Starting Challenge 9")
    
    # 1. Defining the 4x4 Structured Unitary 2 matrix from the PDF
    # Based on the text: 1/2 * [[1, 1, 1, 1], [1, i, -1, -i], [1, -1, 1, -1], [1, -i, -1, i]]
    U = 0.5 * np.array([
        [1, 1, 1, 1],
        [1, 1j, -1, -1j],
        [1, -1, 1, -1],
        [1, -1j, -1, 1j]
    ])
    
    # 2. Initializing the circuit
    qc = QuantumCircuit(2)
    qc.unitary(Operator(U), [0, 1])
    
    # 3. Compiling to Clifford+T basis {h, t, tdg, cx}
    # Using Level 3 optimization since it is the best for finding the most efficient T-gate sequence
    print("Compiling QFT-like structure...")
    optimized_qc = transpile(qc, 
                             basis_gates=['h', 't', 'tdg', 'cx'], 
                             optimization_level=3)
    
    # 4. Generating the QASM output compatible with Qiskit 1.0+
    qasm_output = qasm2.dumps(optimized_qc)
    
    print("\nFINAL OUTPUT\n")
    print(qasm_output)
    
    return qasm_output

# Executing the script
solve_challenge_9()
