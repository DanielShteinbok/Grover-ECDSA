import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler

# Run with simulators
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
# from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# import qiskit_ibm_runtime
# from qiskit_ibm_runtime import QiskitRuntimeService
# from qiskit_ibm_runtime import SamplerV2

from qiskit.visualization import plot_histogram

# from qiskit.circuit.library import QFT

# from qiskit.quantum_info import Statevector
# from qiskit.visualization import plot_bloch_multivector
from Shor_Normal_QFT import *

# need 8 bits
m = 5

multiplierCircuit = QuantumCircuit(2*m+3, m)

# last qubit is just 1 to always force the cMULTmodN to be applied
multiplierCircuit.x(2*m+2)

# initialize to 12
x = 12
# x = 7
# x = 1
for i in range(m):
    bit = (x >> i) & 1
    if bit == 1:
        multiplierCircuit.x(i)

# multiply by 3 mod 13
cMULTmodN(multiplierCircuit, 2*m+2, [*range(m)], [*range(m,2*m+2)], 3, 13, m)

# get modular inverse
# dividerCircuit = QuantumCircuit(2*m+3, m)
# cMULTmodN(dividerCircuit, 2*m+2, [*range(m)], [*range(m,2*m+2)], 1, 13, m)
# multiplierCircuit.compose(dividerCircuit.inverse(), inplace=True)
# multiplierCircuit.draw('mpl')

multiplierCircuit.measure(range(m), range(m))
# plot_histogram(multiplierCircuit, figsize=(10, 5), color='black')
# plt.show()
sampler=AerSampler()
job_sim = sampler.run([multiplierCircuit] , shots=None)
quasi_dists = job_sim.result().quasi_dists[0].binary_probabilities()
print(quasi_dists)

# multiplierCircuit.draw('mpl')
# plot_histogram(quasi_dists)
# plt.show()

