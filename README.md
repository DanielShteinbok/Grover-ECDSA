# (Pretending To) Forge Digital Signatures With A Quantum Computer 
We apply Grover's search to (pretend to) forge ECDSA digital signatures using a quantum computer.

We stand on the shoulders of giants. Namely, much credit is due to Rui Maia and Tiago Leao whose code we have heavily borrowed.
[Their implementation](https://github.com/tiagomsleao/ShorAlgQiskit/tree/master) of [the paper by Stephane Beauregard](https://arxiv.org/abs/quant-ph/0205095) was heavily copy-pasted (with minor modifications) into the file, `Shor_Normal_QFT.py`.