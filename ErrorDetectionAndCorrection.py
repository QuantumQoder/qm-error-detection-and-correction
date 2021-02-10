# This code uses syndrome measurements and makes only two passes to detect errors and correct them.
# The code contains a single Bell pair as the code qubits and a single link bit.
# The errors(identity, x gate, z gate) are introduced in the circuit for each of the two code qubits, thus producing a total of 6 combinations(II, IX, IZ, XI, XX, XZ, ZI, ZX, ZZ)
# The code considers all the 6 combinations and performs correction in each of the cases, if needed.
# The code is also scalable, i.e. it can be extended to more number of code bits.

from qiskit import *

def switch(circuit, i, qubit, reg):
    """Depending on the integer value passed, applies a gate to the reg passed as a parameter to the function.
    
    Args:
        circuit: Contains the memory location of the current quantum circuit
        i: an integer value, depending on which a quantum gate is applied to the circuit
        qubit: an integer value, containing the index of the qubit of the circuit
        reg: contains the information of the register of the circuit
    """
    if i==0:
        circuit.i(reg[qubit])
    elif i==1:
        circuit.x(reg[qubit])
    elif i==2:
        circuit.z(reg[qubit])
    
cq=QuantumRegister(2,'code_qubit')
lq=QuantumRegister(1,'link_qubit')
cb=ClassicalRegister(2,'code_bit')
rlb=ClassicalRegister(2,'round_link_bit')

# This nested loop creates the 6 different combinations of the error gates applied to the two code qubits

for i in list(range(3)):                        # The first loop handles the error gates applied to the first code qubit
    for j in list(range(3)):                    # The second loop handles the error gates applied to the second code qubit
        qc=QuantumCircuit(cq,lq,cb,rlb)
        qc.h(cq[0])                             # Creation of the Bell pair
        qc.cx(cq[0],cq[1])
        switch(qc, i, 0, cq)                    # Applies gate to the first code qubit
        switch(qc, j, 1, cq)                    # Applies gate to the second code qubit
        qc.barrier()
        qc.cx([cq[0],cq[1]],[lq[0],lq[0]])      # first pass of the syndrome measurement
        qc.measure(lq[0],rlb[0])                # bit-flips one of the code bit if it detects an error in the two
        qc.x(cq[1]).c_if(rlb,1)
        qc.barrier()
        qc.reset(lq[0])
        qc.cx([cq[0],cq[1]],[lq[0],lq[0]])      # second pass rechecks the error in the code qubits
        qc.measure(lq[0],rlb[1])
        qc.measure(cq,cb)
        print('\n\t\t\t========= circuit[',i,'][',j,']=========\n')
        print(qc)
        job = execute( qc, Aer.get_backend('qasm_simulator') )
        print(job.result().get_counts(qc))
