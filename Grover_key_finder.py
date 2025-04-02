from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import DraperQFTAdder, IntegerComparator, QFT, RGQFTMultiplier
from Shor_Normal_QFT import *
from PyECCArithmetic import *
# import math

class Curve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

def add_modp(p):
    """
    make a circuit that adds two quantum integers mod p
    """
    # want p.bitlength() bits to represent x,
    # want p.bitlength() +1 bits to represent y,
    # and 2 ancillary bits for the carry
    circuit = QuantumCircuit(2*p.bit_length()+2)

    # add the two numbers, carrying
    circuit.append(DraperQFTAdder(p.bit_length(), kind='half').to_instruction(), 
                   [*range(p.bit_length())] + 
                   [*range(p.bit_length()+1, 2*p.bit_length()+1)] + 
                   [p.bit_length()]) 
    
    # apply comparator with output on the last bit
    circuit.append(IntegerComparator(p.bit_length()+1, value=p).to_instruction(),
                   [*range(p.bit_length(), 2*p.bit_length()+2)])

    # depending on the value of the comparator, subtract p
    # circuit.append(
    #     DraperQFTAdder(p.bit_length(), kind='half').to_instruction()
    #     .inverse().control(1), [2*p.bit_length()+1] 
    #     + [*range(p.bit_length())] 
    #     + [*range(p.bit_length()+1, 2*p.bit_length()+1)] 
    #     + [p.bit_length()]
    # )
    # do a QFT so that our subtraction works
    circuit.compose(QFT(p.bit_length() + 1), [*range(p.bit_length(), 2*p.bit_length()+1)])
    # do the inverse addition of a constant, which is subtraction
    # this is controlled by the last bit, which is the result of the comparator
    cphiADD(circuit, [*range(p.bit_length(), 2*p.bit_length()+1)], [2*p.bit_length()+1], p, p.bit_length()+1, inv=1)
    circuit.compose(QFT(p.bit_length() + 1, inverse=True), [*range(p.bit_length(), 2*p.bit_length()+1)])

    return circuit

def montgomery_modular_mult(p, R=None):
    """
    Performs a modular multiplication using Montgomery forms
    Assumes that the inputted numbers are already in montgomery form
    Assumes R is 2^n where p is an n-bit integer
    """
    if R is None:
        R = pow(2, p.bit_length())
    R_inv = pow(R, -1, p)

    # I know I'll use RGQFTMultiplier first to multiply the numbers
    # but then the next question is how I'll do a modular multiplication by R_inv
    # The simple stupid method is to have an extra |1> qubit and just use the cMULTmodN that I already have
    # the latter requires 2n+2 qubits, and with the 1 qubit it's 2n+3
    # where n is the number of qubits after multiplication
    # actually, I just added an uncontrolled multiplication for which we don't need that extra qubit
    circuit = QuantumCircuit(p.bit_length()*6 + 2)

    # last qubit is 1 to force modular multiplication
    # circuit.x(p.bit_length()*4 + 2)
    # don't need to do that anymore
    # first, multiply the two
    circuit.append(RGQFTMultiplier(p.bit_length()).to_instruction(), [*range(p.bit_length()*4)])

    # then modularly multiply by the inverse R
    MULTmodN(circuit, [*range(p.bit_length()*2, p.bit_length()*4)], [*range(p.bit_length()*4, p.bit_length()*6+2)], R_inv, p, p.bit_length()*2)

    return circuit


# def uf_oracle(m, Q, curve, G, n):
def uf_oracle(Q, G, curve=Curve(a=0, b=7, p=13), k_bits=None):
    """
    Generates an oracle U:|k>|d>|0> --> |k>|d>|k*d==Q>.
    That is, the last qubit becomes 1 if k*d == Q mod p, and 0 otherwise.
    d is the representation of the point on the curve, and is the private key.
    k is an integer
    Essentially, the last qubit becomes 1 if the private key is the correct one.
    """
    if k_bits is None:
        k_bits = int(curve.p).bit_length()

    # we have 3 integers: k, d[0], d[1] 
    # where d[0] and d[1] are the x and y coordinates of the point on the curve
    # circuit = QuantumCircuit(3*k_bits + 1)
    G_powers_array = []
    for i in range(k_bits):
        pass
        # TODO: calculate the multiples of G*pow(2, i)
    
    # create a circuit
    # for each qubit in the circuit, add the appropriate power of G
    # check whether the result is equal to Q, do a multi-controlled-x across all bits to target the bottom, target qubit

    
def generate_key_finder_circuit(Q, curve, G, n, uf_oracle, iterations=1):
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
