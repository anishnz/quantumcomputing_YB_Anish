"""
Task 2 - ALTERNATIVE version: both Task 2 circuits built with Cirq instead of Qiskit/QASM.

Part A: H on q0, X on q1, block C = CNOT(q0 -> q1)  -> Bell state |Psi+> = (|01> + |10>)/sqrt(2)
Part B: our quantum half adder (A, B in superposition; CARRY = A AND B; SUM = A XOR B)

Each circuit is run twice:
  1. Cirq's own simulator (completely independent of Qiskit)
  2. exported to QASM and sent to Quokka (or the labelled local fallback)

Run:   python Alternative_Code/Task_2_Alt_Cirq/task2_circuits_cirq.py
"""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import qh, OUTPUTS, SHOTS, banner

import cirq                                            # Google's quantum library


def cirq_counts(circuit, key, n_bits):
    """Run on Cirq's simulator and return counts in Qiskit order (highest bit on the left)."""
    result = cirq.Simulator(seed=802).run(circuit, repetitions=SHOTS)   # fixed seed -> repeatable
    rows = result.measurements[key]                    # one row per shot: [bit0, bit1, ...]
    return dict(sorted(Counter("".join(str(b) for b in reversed(r[:n_bits])) for r in rows).items()))


# ------------------------------------------------------------------ Part A
banner("Task 2A (alternative): H, X, then C = CNOT, built in Cirq")
q0, q1 = cirq.LineQubit.range(2)
part_a = cirq.Circuit(cirq.H(q0),            # superposition on the top line
                      cirq.X(q1),            # bottom line set to |1>
                      cirq.CNOT(q0, q1),     # block C: q1 = q1 XOR q0
                      cirq.measure(q0, q1, key="c"))
print(part_a)
print("Cirq simulator counts :", cirq_counts(part_a, "c", 2))          # expect only 01 and 10
run_a = qh.run_qasm(cirq.qasm(part_a), shots=SHOTS, label="alt_task2a_cirq", save_dir=OUTPUTS)
print(f"{run_a['source'][:15]:<15} counts :", run_a["counts"])

# ------------------------------------------------------------------ Part B
banner("Task 2B (alternative): quantum half adder, built in Cirq")
a, b, carry, s = cirq.LineQubit.range(4)
part_b = cirq.Circuit(
    cirq.H(a), cirq.H(b),                  # inputs in superposition: all 4 additions at once
    cirq.Z(a), cirq.S(b),                  # phase gates: change amplitudes, not probabilities
    cirq.TOFFOLI(a, b, carry),             # CARRY = A AND B
    cirq.CNOT(a, s), cirq.CNOT(b, s),      # SUM = A XOR B
    cirq.measure(a, b, carry, s, key="c"))
print(part_b)
counts_b = cirq_counts(part_b, "c", 4)
print("Cirq simulator counts :", counts_b)                               # expect 0000, 1001, 1010, 0111
run_b = qh.run_qasm(cirq.qasm(part_b), shots=SHOTS, label="alt_task2b_cirq", save_dir=OUTPUTS)
print(f"{run_b['source'][:15]:<15} counts :", run_b["counts"])

print("\nTruth-table check (string = SUM CARRY B A):")
for key, n in counts_b.items():
    s_bit, c_bit, b_bit, a_bit = (int(x) for x in key)
    ok = s_bit == (a_bit ^ b_bit) and c_bit == (a_bit & b_bit)
    print(f"  {key}:  {a_bit} + {b_bit} = carry {c_bit}, sum {s_bit}   x{n:<4} {'correct' if ok else 'WRONG'}")
