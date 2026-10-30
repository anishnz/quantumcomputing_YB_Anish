// =====================================================================
// MSE802 Assessment 2 - Task 2 Part B : our own circuit, written in QASM
// "Quantum half adder in superposition"
// Group project: Anish Shrestha and Sandhya Tiwari
//
// Qubit roles:  q[0] = A (input)   q[1] = B (input)
//               q[2] = CARRY (A AND B)   q[3] = SUM (A XOR B)
// Idea: H gates put A and B into superposition, so ONE circuit adds
// 0+0, 0+1, 1+0 and 1+1 at the same time. Each shot shows one of them.
// =====================================================================
OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];              // four qubits, all start in |0>
creg c[4];              // four classical bits for the results

h q[0];                 // A -> (|0> + |1>)/sqrt(2)
h q[1];                 // B -> (|0> + |1>)/sqrt(2)
z q[0];                 // phase flip: A becomes (|0> - |1>)/sqrt(2); probabilities do NOT change
s q[1];                 // S = quarter-turn phase on B: (|0> + i|1>)/sqrt(2); probabilities do NOT change
barrier q;              // visual separator (ignored by the hardware)

ccx q[0],q[1],q[2];     // Toffoli: CARRY flips to 1 only when A = 1 AND B = 1
cx q[0],q[3];           // SUM = SUM XOR A
cx q[1],q[3];           // SUM = SUM XOR B  ->  SUM = A XOR B
barrier q;

measure q[0] -> c[0];   // read A
measure q[1] -> c[1];   // read B
measure q[2] -> c[2];   // read CARRY
measure q[3] -> c[3];   // read SUM
