from qiskit import QuantumCircuit

# Circuito a 2 qubit
qc = QuantumCircuit(2)

# Blocco T² su q1
qc.t(1)
qc.t(1)

# H T⁴ H su q1 (T⁴ = quattro T)
qc.h(1)
qc.t(1)
qc.t(1)
qc.t(1)
qc.t(1)
qc.h(1)

# T†² su q1
qc.tdg(1)
qc.tdg(1)

# CNOT q0 -> q1
qc.cx(0,1)

# Disegno del circuito
print(qc.draw())

