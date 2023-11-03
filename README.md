# qm-error-detection-and-correction

- This code uses syndrome measurements and makes only two passes to detect errors and correct them.
- The code contains a single Bell pair as the code qubits and a single link bit.
- The errors(identity, ***X***, ***Z***) are introduced in the circuit for each of the two code qubits, thus producing a total of 9 combinations(***II***, ***IX***, ***IZ***, ***XI***, ***XX***, ***XZ***, ***ZI***, ***ZX***, ***ZZ***)
- The code considers all the 9 combinations and performs correction in each of the cases, if needed.
- The code is also scalable, i.e. it can be extended to more number of code bits.
