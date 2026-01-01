# QPE implementation and scaling study
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute

backend = Aer.get_backend("qasm_simulator")

# -------------------------------------------------
# Quantum Fourier Transform
# -------------------------------------------------
def qft(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
        for j in range(i + 1, n):
            qc.cp(np.pi / 2**(j - i), j, i)
    qc.swap(0, n - 1)
    return qc

# -------------------------------------------------
# Quantum Phase Estimation
# -------------------------------------------------
def qpe(n_count, phase):
    qc = QuantumCircuit(n_count + 1, n_count)
    qc.x(n_count)

    for i in range(n_count):
        qc.h(i)
        qc.cp(2 * np.pi * phase * (2**i), i, n_count)

    qc.append(qft(n_count).inverse(), range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc

# -------------------------------------------------
# Phase extraction
# -------------------------------------------------
def estimate_phase(counts, n_count):
    bitstring = max(counts, key=counts.get)
    return int(bitstring, 2) / (2**n_count)

# -------------------------------------------------
# Accuracy scaling
# -------------------------------------------------
if __name__ == "__main__":

    true_phase = 0.125
    errors = []

    for n in range(2, 8):
        qc = qpe(n, true_phase)
        result = execute(qc, backend, shots=4096).result()
        counts = result.get_counts()

        est = estimate_phase(counts, n)
        err = abs(est - true_phase)
        errors.append(err)

        print(f"Qubits: {n} | Estimated phase: {est:.4f} | Error: {err:.2e}")

    plt.semilogy(range(2, 8), errors, 'o-')
    plt.xlabel("Counting Qubits")
    plt.ylabel("Phase Error")
    plt.title("QPE Phase Error vs Counting Qubits")
    plt.grid()
    plt.show()

