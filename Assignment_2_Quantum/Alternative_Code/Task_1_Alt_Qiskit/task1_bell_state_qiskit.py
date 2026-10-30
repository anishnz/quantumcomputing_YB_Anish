"""
Task 1 - ALTERNATIVE version: the same Bell state built with Qiskit instead of Cirq.

Why an alternative? It shows the result does not depend on the library:
Cirq and Qiskit both produce the same OpenQASM, and Quokka sees the same script.

Run:   python Alternative_Code/Task_1_Alt_Qiskit/task1_bell_state_qiskit.py
Output: counts printed in the terminal + Alternative_Code/outputs/alt_task1_*.png/json
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # reach Alternative_Code/_common.py
from _common import qh, OUTPUTS, SHOTS, banner                 # shared helper + output folder

import matplotlib
matplotlib.use("Agg")                                  # save charts to files (no window needed)
import qiskit.qasm2                                    # Qiskit -> OpenQASM 2.0 text
from qiskit import QuantumCircuit                      # circuit object
from qiskit.quantum_info import Statevector            # exact state for the theory check

banner("Task 1 (alternative): Bell state |Phi+> with Qiskit")

qc = QuantumCircuit(2, 2)        # 2 qubits + 2 classical bits, all start at 0
qc.h(0)                          # Hadamard on q0 -> (|0> + |1>)/sqrt(2)
qc.cx(0, 1)                      # CNOT q0 -> q1 -> (|00> + |11>)/sqrt(2)
print(qc.draw("text"))

# ---- theory: exact probabilities from the state vector ----
ideal = Statevector(qc).probabilities_dict()           # {'00': 0.5, '11': 0.5}
print("Theory probabilities:", {str(k): round(float(v), 3) for k, v in ideal.items()})

# ---- measurement on Quokka (or the labelled local simulator) ----
qc.measure([0, 1], [0, 1])                             # read both qubits
run = qh.run_qasm(qiskit.qasm2.dumps(qc), shots=SHOTS, label="alt_task1_bell_qiskit", save_dir=OUTPUTS)
print("Source :", run["source"])
print("Counts :", run["counts"])

# ---- quick checks ----
correlated = run["counts"].get("00", 0) + run["counts"].get("11", 0)
print(f"Correlated shots (00 or 11): {correlated} / {run['shots_received']}")
print("TVD theory vs measured:", round(qh.total_variation_distance(ideal, run["probs"]), 4))

qh.plot_comparison({"Theory": ideal, "Measured": run["probs"]},
                   "Alternative Task 1 (Qiskit): Bell state", path=OUTPUTS / "alt_task1_histogram.png")
print("Saved chart:", OUTPUTS / "alt_task1_histogram.png")
