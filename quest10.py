#author: EnesV
import numpy as np
from qiskit import QuantumCircuit, transpile, qasm2
from qiskit.quantum_info import random_unitary

def solve_challenge_10():
    print("Starting Challenge 10")
    
    try:
        u_random = random_unitary(4, seed=42)
        print("Target unitary generated successfully.")
        
        # 1. Building the circuit
        qc = QuantumCircuit(2)
        qc.unitary(u_random, [0, 1])
        
        # 2. Transpiling to the required gate set {h, t, tdg, cx} 
        # Optimization level 3 helps minimize T-count 
        print("Compiling to Clifford+T...")
        optimized_qc = transpile(qc, 
                                 basis_gates=['h', 't', 'tdg', 'cx'], 
                                 optimization_level=3)
        
        # 3. Generating the QASM string
        # Using qasm2 for compatibility with Qiskit 1.0+
        qasm_output = qasm2.dumps(optimized_qc)
        
        print("\nFINAL QASM OUTPUT\n")
        print(qasm_output)
        print("\n End of Output")
        
        return qasm_output

    except Exception as e:
        print(f"An error occurred: {e}")

# Runing the function
output = solve_challenge_10()
