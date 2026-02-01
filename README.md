# QUHACK Submission Report

- Git repository: darolo95/QUHACK (collaborators: ItzEnes, darolo95, xbluegalaxyx)
- Authors: E. YILDIZ & D. Tafrishi - xbluegalaxyx - Team Quackers
- Contest: MIT IQuHack 2026
- Date: 2026-02-01

---

## Overview

This repository contains Python solutions (`quest1.py` through `quest4.py`, with verifiers and helpers for subsequent challenges) for the QUHACK challenge problems. Each file implements quantum circuits or algorithms using Qiskit and focuses on fault-tolerant compilation, approximate synthesis, and Hamiltonian exponentiation under the Clifford+T constraint. Circuits were exported to OpenQASM 2.0 restricted to the gate set {H, T, T†, CNOT} as required.

A literature review and an online workshop undertaken at the start of the challenge were fundamental to understanding qubit dynamics in quantum circuits and to tackling the compilation, approximation, and synthesis challenges. In particular, Ross & Selinger [1] guided our approach for Clifford+T approximations of Z-rotations.

---

## Files of interest

- `quest1.py` - Controlled-Y (`CY`) sanity-check and Clifford+T optimization
- `quest2.py` - Controlled-Ry(π/7) synthesis and approximation
- `quest3.py` - Synthesis of e^{i π/7 Z⊗Z} via approximate Rz rotations
- `quest4.py` - Exponential of H1 = XX + YY; Hamiltonian exponentiation & compilation
- `verify_q5`, `verify_q6`, `verify_q7`, `verify_q8`, `verify_q9`, `verify_q10`, `verify_q11` - verification / challenge helper scripts referenced in the report
- Additional helper modules: basis-change utilities, custom Clifford+T translators (e.g., `clean_rz_sequence`), and OpenQASM exporters

---

## Quest 1 - Controlled‑Y Gate

Objective
- Sanity check: construct and synthesize a Controlled‑Y (`CY`) Clifford unitary; optimize operator norm distance and T‑count in a 2‑qubit space.

Approach
- Implemented `CY` using Qiskit primitives (degenerate case related to Controlled‑Ry(π)).
- Used Qiskit synthesis and custom postprocessing to optimize matrices and reduce gate count through Pauli-basis conversions.
- Replaced non‑allowed Clifford gates (S/S†) with T/T† sequences where necessary using a custom mapping (e.g., `clean_rz_sequence`) to ensure exact compliance with the gate set.

Circuit highlights
- Qiskit constructs used: `QuantumCircuit`, `cx`, `h`, `t`, `tdg`.
- Final OpenQASM output restricted to {H, T, T†, CNOT}.

Results
- Circuit depth (reported): ~1.73
- T count: 4

Reference: `quest1.py`

---

## Quest 2 - Controlled‑Ry(π/7)

Objective
- Build a controlled rotation around Y: Controlled‑Ry(π/7). Optimize operator norm distance and T‑count.

Approach
- Implemented Controlled‑Ry(π/7) in `quest2.py`.
- Used Qiskit’s gridsynth-like techniques for Rz approximation (gridsynth_rz style) and basis rotations to convert Ry into Rz-type rotations when needed.
- Replaced S / S† gates by equivalent T / T† sequences consistent with a strict T budget:
  - S -> T·T
  - S† -> T†·T†
- Multi‑qubit Z rotations implemented via CNOT chains and single-qubit T / T† gates (Pauli rotation gadgets).
- Set approximation error ε to trade accuracy vs T-count as required by the challenge.

Methodology & optimizations
- Converted target unitary to Pauli basis and identified Rz components for synthesis.
- Grouped terms to minimize redundant Clifford basis changes and merged multi‑qubit rotations where possible.

Results
- Achieved operator norm below 1 (per reported metric) at the cost of ~75 T gates.
- Generated OpenQASM containing only the allowed gate set.

Reference: `quest2.py`

---

## Quest 3 - Exponential of a Pauli string: e^{i π/7 Z⊗Z}

Objective
- Synthesize a two‑qubit circuit implementing e^{i π/7 Z⊗Z} with low operator norm distance and reduced T‑count.

Approach
- Implemented in `quest3.py` using approximate Rz(θ) synthesis (gridsynth_rz style) for single‑qubit rotations with an allowed approximation ε (example ε = 0.1 for Rz(2π/7) synthesis).
- Employed CNOT–Rz–CNOT embedding pattern to implement two‑qubit controlled rotations.
- Maintained the same S/S† → T/T† replacement strategy for strict gate‑set compliance.

Results
- Produced an approximate Clifford+T decomposition satisfying the chosen error tolerance.
- T count reported: 26 (substantially lower than the Controlled‑Ry(π/7) example).
- OpenQASM output preserves the allowed gate set.

Reference: `quest3.py`

---

## Quest 4 - Exponential of H1 = XX + YY : e^{i π/7 H1}

Objective
- Use algebraic/exponential properties to implement e^{i π/7 (XX + YY)} and optimize both distance and T‑count.

Approach
- Implemented base circuit using Qiskit primitives and performed classical preprocessing where helpful (e.g., diagonalization, eigenvalue analysis).
- Mapped XX/YY terms into implementable circuits via basis rotations (Hadamard / S‑like transforms) and applied standard CNOT‑based phase gadgets.
- Compiled resulting circuits into Clifford+T using custom translation functions; exported to OpenQASM with allowed gates.

Outcome
- Valid OpenQASM output restricted to {H, T, T†, CNOT}.
- Circuit verified by simulation for correctness.

Reference: `quest4.py`

## Quest 4 - Exponential of H1 = XX + YY : e^{i π/7 H1} - BIS_xbluegalaxyx
I have diagonalized this Hamiltonian matrix H1 along the Z axis by using the Rz(theta) function to make sure that the axis of rotation of the particle is minimum. This also makes sure that the axis of rotation is not a multiple of pi/4, which is the characteristics of a T-gate. This ensure that minimum number of T-gates are used. 
Mathematically, I wrapped the Hamiltonian matrix H1 by the gates H (Hadamard) and the S gate (Phase gate) twice to obtain the result Z XOR Z, diagonalized along the Z axis. Then we exponentiated it and passed it into the Rz() function with a multiple of 2, which essentially negates the 2 factor in the denominator in the default Rz() function. Then we sandwiched it with CNOT (Controlled-Not) function to create a control and target qubit: Clifford-T  universal gates. 
Identity Used: CNOT – Rz(2theta) – CNOT
Computationally, I implemented this logic in a .qasm file using the OPENQASM 2.0 version. Then I wrote a python file to test the simulation of this quantum circuit by calling upon the .qasm file. I used the library function such as qiskit, qiskit,quantum_into and numpy to its essential functions. 
Result: The number of T gates used initially was 14 and after optimization with the new logic came down to 8. 


---

## Quest 5 - Isotropic Heisenberg Evolution (H2 = XX + YY + ZZ)

Unitary
- U = exp(i (π/2) H2), where H2 = XX + YY + ZZ.

Analysis & insight
- The isotropic Heisenberg operator exp(i (π/2) (XX + YY + ZZ)) is equivalent to the identity up to a global phase on two qubits.
- As a result, the evolution produces no change to the state vector (only a global phase), so the implemented operation is effectively the identity.

Implementation
- Because the operator acts as global-phase-only for the specified angle, the realized circuit is the identity; T‑count and gate counts are zero.

Reference: `verify_q5` and Challenge 5 helper scripts

---

## Quest 6 - Transverse Field Ising Model (TFIM)

Unitary
- exp(i (π/7) H3) where H3 = XX + ZI + IZ.

Analysis
- The three terms commute on 2 qubits; therefore the exponential factorizes:
  exp(i (π/7) H3) = exp(i (π/7) XX) · exp(i (π/7) ZI) · exp(i (π/7) IZ).

Compilation
- ZI and IZ compiled as single‑qubit Rz(−2π/7) rotations on the appropriate qubits.
- XX term mapped into ZZ basis via Hadamard transforms (H X H = Z), then implemented using a CNOT‑based phase gadget for exp(i θ ZZ).

Reference: `verify_q6` and Challenge 6 helper scripts

---

## Quest 7 - Arbitrary State Preparation

Task
- Synthesize a unitary U ∈ C^{4×4} such that |00⟩ ↦ |ψ_target⟩ where |ψ_target⟩ was generated by `qiskit.quantum_info.random_statevector(4, seed=42)`.

Analysis & compilation
- Prepared the target state via sequential amplitude zeroing rotations (standard state‑preparation procedure).
- Prioritized operator norm distance (high fidelity) over T‑count when transpiling into Clifford+T to ensure the target state was reached accurately.
- Final unitary was transpiled and exported in the allowed gate set.

Reference: `verify_q7` and Challenge 7 helper scripts

---

## Quest 8 - Structured Unitary 1

Task
- Efficiently compile a structured unitary by identifying underlying structure (permutation / Clifford‑heavy).

Discovery & result
- Identified the unitary as effectively a Clifford-equivalent operation (e.g., SWAP or controlled‑Z variant).
- By exploiting the Clifford structure, produced a circuit with T‑count ≈ 0 and zero operator distance (exact).

Reference: `verify_q8` and Challenge 8 helper scripts

---

## Quest 9 - Structured Unitary 2 (QFT Structure)

Unitary
- The provided 4×4 matrix matches the 2‑qubit Quantum Fourier Transform (QFT):
<details open>
<summary><strong>Matrix </strong></summary>

$$
\frac{1}{2}
\begin{pmatrix}
1 & 1 & 1 & 1 \\
1 & i & -1 & -i \\
1 & -1 & 1 & -1 \\
1 & -i & -1 & i
\end{pmatrix}
$$

</details>


Analysis & compilation
- QFT decomposition: Hadamards plus controlled phase rotations CP(π/2).
- CP(π/2) decomposed exactly into Clifford+T using CNOT, T and T†, yielding a very low T‑count.

Reference: `verify_q9` and Challenge 9 helper scripts

---

## Quest 10 - Random Unitary (Seed 42)

Unitary
- Generated with `qiskit.quantum_info.random_unitary(4, seed=42)`.

Analysis & compilation
- Random unitaries generally lack exploitable structure. We used the `rmsynth` approach (multi-pass optimization) to synthesize an optimized Clifford+T sequence.
- Performed multiple passes to balance T‑count and approximation accuracy; achieved T‑count < 50 while keeping distance d(U,Ũ) < 1e‑4.

Reference: `verify_q10` and Challenge 10 helper scripts

---

## Quest 11 - 4‑Qubit Diagonal Unitary

Task
- Compile the diagonal unitary U|x⟩ = e^{i φ(x)} |x⟩ for 4 qubits (16 basis states) with specified phases (ranging from 0 to 7π/4, including values like 5π/4 and 3π/2).

Compilation approach
- Converted the phase function into a phase polynomial representation.
- Implemented using:
  - CNOT parity network to compute relevant parities,
  - T and T† rotations on parity wires,
  - Uncompute the parity network.
- This representation minimizes the number of non‑Clifford gates while leveraging the diagonal structure.

Reference: `verify_q11` and Challenge 11 helper scripts

---

## General notes

- All circuits were exported in OpenQASM 2.0 format.
- Gate set for exported circuits strictly restricted to {H, T, T†, CNOT}.
- When approximations were used (e.g., for single‑qubit rotations), error bounds were respected as per challenge specifications.
- Commuting Pauli rotations were diagonalized in an appropriate basis to reduce T‑count via merged rotations and shared basis changes.
- Where exact decomposition into Clifford+T is possible (Clifford-only operations), we produced T‑free implementations.

---

## Conclusion

By leveraging unitary structure (commutation properties, diagonalizations, and Clifford identities) together with advanced synthesis tools like rmsynth and gridsynth-like approximations for Rz, we compiled the challenge unitaries into high‑fidelity Clifford+T sequences. The results show that even for random or complex unitaries, careful decomposition and basis choice can substantially reduce fault‑tolerant costs (T‑count) while meeting operator distance constraints.

---

## References

[1] N. J. Ross and P. Selinger, “Optimal ancilla‑free Clifford+T approximation of z‑rotations”, arXiv:1403.2975 (2014).

---

For implementation details, circuit listings, and exported OpenQASM files, see the corresponding scripts:
`quest1.py`, `quest2.py`, `quest3.py`, `quest4.py`, and the `verify_q*` helper scripts in this repository.
