from qiskit import QuantumCircuit, transpile, qasm2
import numpy as np

# Example 2‑qubit unitary
U = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,-1j],
    [0,0,1j,0]
])

qc = QuantumCircuit(2)
qc.unitary(U, [0, 1])

qc_t = transpile(qc, basis_gates=['h','s','t','cx'], optimization_level=3)

# Export to OpenQASM 2 string
qasm_str = qasm2.dumps(qc_t)

# Write to file
with open("unitary_cliffordT.qasm", "w") as file:
    file.write(qasm_str)

print("Saved Clifford+T QASM to unitary_cliffordT.qasm")
