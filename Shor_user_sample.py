import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler

# Run with simulators
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# import qiskit_ibm_runtime
# from qiskit_ibm_runtime import QiskitRuntimeService
# from qiskit_ibm_runtime import SamplerV2

from qiskit.visualization import plot_histogram

from qiskit.circuit.library import QFT

from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from Shor_Normal_QFT import *

# need 7 bits to represent 0-127 for the part we throw away
m = 7

# We should get s/16 for some integer s, 
# so we actually need 4 bits to represent
# but then we'd just see an equally-divided result of all possible outcomes
# which does not look so nice. Let's use 5 bits instead,
# and we'll see the solutions skip a bit.
n = 5

# our first guess is a = 3, which should have an order of 16
a = 3
N = 85


shor_circuit = QuantumCircuit(n + 2*m+2, n)

#  the modular multiplication requires a bunch of extra qubits
# aux = QuantumRegister(m+2)

# Apply Hadamard gates to the counting qubits
for i in range(n):
    shor_circuit.h(i)

shor_circuit.x(n + m - 1)
# Apply whatever U we want to implement
for i in range(n):
    # for j in range(2**i):
        # example U gate: multiply by 2 mod 15
        # controlled_U = control_U(2, 15, m)
    # qpe_circuit.append(controlled_U, [i] + [*range(n, n + m + 1)])
    cMULTmodN(shor_circuit, i, [*range(n, n + m)], [*range(n+m,n+2*m+2)], pow(a, 2**i, N), N, m)

shor_circuit = shor_circuit.compose(QFT(n, inverse=True), qubits=range(n))

# plot_bloch_multivector(Statevector(qft_circuit))
# state_pre_measure = Statevector(qft_circuit)

shor_circuit.measure(range(n), range(n))

sampler=AerSampler()
job_sim = sampler.run([shor_circuit] , shots=None)
quasi_dists = job_sim.result().quasi_dists[0].binary_probabilities()

plot_histogram(quasi_dists)
