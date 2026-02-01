#author: EnesV
from qiskit import QuantumCircuit, transpile, qasm2
from qiskit.quantum_info import random_statevector
from qiskit.circuit.library import StatePreparation

def solve_challenge_7():
    # Generating the specific statevector from the challenge PDF
    target_state = random_statevector(4, seed=42)
    
    qc = QuantumCircuit(2)
    sp_gate = StatePreparation(target_state)
    qc.append(sp_gate, [0, 1])
    
    # Decomposing into Clifford+T
    basis_gates = ['h', 't', 'tdg', 'cx']
    final_qc = transpile(qc, basis_gates=basis_gates, optimization_level=3)
    
    print(qasm2.dumps(final_qc))
    return final_qc

solve_challenge_7()
