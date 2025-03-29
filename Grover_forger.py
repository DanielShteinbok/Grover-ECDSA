from qiskit import QuantumCircuit

def generate_forger_circuit(m, Q, curve, G, n, uf_oracle, iterations=1):
    """
    Generates a quantum circuit for the Grover forger algorithm.
    
    Parameters:
    ----------
        m: The (hash of) the message for which a signature is to be forged.
        Q: The public key for which we want to forge.
        curve: The elliptic curve used for the forgery.
        G: The base point on the elliptic curve.
        n: The integer order of G.
        iterations: The number of iterations for Grover's algorithm.
    
    Returns:
    -------
        circuit: A QuantumCircuit object representing the Grover forger circuit.
    """
    N = int(n).bit_length()  # Number of bits needed to represent n
    # N is significatn because it tells us how many bits we need to represent r and s which are both mod n
    # we need 2*N bits to represent both r and s
    
    circuit = QuantumCircuit(2*N + 1, 2*N)

    circuit.x(N)
    circuit.h(range(2*N))

    for i in range(iterations):
        circuit.append(uf_oracle(), range(2*N+1))
        circuit.h(range(2*N))
        circuit.x(range(2*N))

        # no multi-controlled Z available, so we use multi-controlled X
        # and we use the fact that Z = HXH
        circuit.h(2*N-1)
        circuit.mcx(list(range(2*N-1)), 2*N-1)
        circuit.h(2*N-1)

        circuit.x(range(2*N))
        circuit.h(range(2*N))

    circuit.measure(range(2*N), range(2*N))
    return circuit
