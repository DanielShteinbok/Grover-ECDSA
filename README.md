<!-- # (Pretending To) Forge Digital Signatures With A Quantum Computer 
We apply Grover's search to (pretend to) forge ECDSA digital signatures using a quantum computer.

We stand on the shoulders of giants. Namely, much credit is due to Rui Maia and Tiago Leao whose code we have heavily borrowed.
[Their implementation](https://github.com/tiagomsleao/ShorAlgQiskit/tree/master) of [the paper by Stephane Beauregard](https://arxiv.org/abs/quant-ph/0205095) was heavily copy-pasted (with minor modifications) into the file, `Shor_Normal_QFT.py`. -->
# (Pretending To) Steal ECC Keys With A Quantum Computer 
Previously, the intention was to just forge signatures. 
However, it turns out that our approach to that required a quantum implementation of elliptic curve multiplication,
at which point we could just steal the key altogether. This would be simpler and cooler.

We stand on the shoulders of giants. Namely, much credit is due to Rui Maia and Tiago Leao whose code we have heavily borrowed.
[Their implementation](https://github.com/tiagomsleao/ShorAlgQiskit/tree/master) of [the paper by Stephane Beauregard](https://arxiv.org/abs/quant-ph/0205095) was heavily copy-pasted (with minor modifications) into the file, `Shor_Normal_QFT.py`.

## The Algorithm
Fundamentally, we use a Grover's search to find a private key. 
Grover's search allows you to essentially reverse any computation, 
so long as you can formultate it as a unitary $U_f$ which tells you whether or not you have succeeded.

Suppose you have $f$:
$$
f = \begin{cases}
1 & \text{$x$ is `correct'; in our case, $x$ is the private key} \\
0 & \text{otherwise}
\end{cases}
$$

Then you define $U_f|x\rangle|0\rangle = |x\rangle|f(x)\rangle$ with which you can perform Grover's algorithm. The crux is actually formulating the $U_f$ in practice!

In our case, we want to reverse an elliptic curve multiplication $x\times G$ where $x$ is a scalar and $G$ is a point on the elliptic curve.

To do this kind of efficiently, we use the double-and-add method, and precompute $\{2^kG|k=0,1,...,n-1\}$ classically. We then find that, if $x_k\in\{0,1\}$ is the $k$-th bit of $x$ (starting from $k=0$), we have,
$$
x\times G = \sum_{i=0}^{n-1}x_k2^kG
$$
In essence, this reduces the problem to repeated point addition of the precomputed $2^kG$ controlled by the bits of $x$. 
<!-- This controlled point addition is described by [(Roetteler et al, 2017)](https://arxiv.org/abs/1706.06752) as:
1. $x_1 \leftarrow x_1 - x_2 \mod p$
2. $y_1 \leftarrow y_1 - y_2\cdot c \mod p$
3. $t_0 \leftarrow (x_1 - x_2)^{-1} \mod p$
4. $\lambda \leftarrow y_1/x_1 \mod p$ -->
Point addition can be performed by doing the following:
$$
\lambda = (y_2 - y_1)\cdot(x_2 - x_1)^{-1} \mod p \\
x_3 = \lambda^2 - x_2 - x_1 \mod p \\
y_3 = -(y_1 + \lambda(x_3 - x_1)) \mod p
$$

For computing the multiplicative inverse, we use the inverse of the controlled-multiplication gate by the aforementioned giants. For multiplying quantum variables together, we should use their Montgomery forms.