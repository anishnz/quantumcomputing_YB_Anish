"""
Task 4 - ALTERNATIVE version: the same bars-vs-stripes circuit, trained a different way.

Differences from the main notebook:
  * the circuit is built as a Qiskit QuantumCircuit (not QASM text),
  * its output P(q3 = 1) is computed EXACTLY with Qiskit's Statevector (no device, no shots),
  * a different optimiser is used: SciPy's COBYLA (gradient-free, deterministic).
It shows that the circuit, not the optimiser, is what solves the problem.

Run:   python Alternative_Code/Task_4_Alt_Statevector/task4_classifier_statevector.py
Output: loss per iteration in the terminal + outputs/alt_task4_*.png/csv
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import OUTPUTS, banner

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

banner("Task 4 (alternative): exact Statevector classifier + COBYLA optimiser")

# ---- the 4 images (same as the notebook: label 0 = 'stripes', 1 = 'bars') ----
images = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1]])
labels = np.array([0, 0, 1, 1])
PAIRS = [(0, 1), (2, 3), (1, 3)]                    # tree of blocks, same as generate_pairs(0, 3)


def build(image, theta):
    """Input encoding (X gates) + 3 trainable RY-RY-CNOT blocks."""
    qc = QuantumCircuit(4)
    for i, pixel in enumerate(image):
        if pixel:
            qc.x(i)                                  # white pixel -> |1>
    for b, (i, j) in enumerate(PAIRS):
        qc.ry(theta[2 * b], i)
        qc.ry(theta[2 * b + 1], j)
        qc.cx(i, j)
    return qc


def predict(theta, image):
    return Statevector(build(image, theta)).probabilities([3])[1]   # exact P(q3 = 1)


history = []
t_start = time.perf_counter()


def loss(theta):
    value = float(np.mean([abs(predict(theta, x) - y) for x, y in zip(images, labels)]))
    history.append({"evaluation": len(history) + 1, "loss": value, "time_s": time.perf_counter() - t_start})
    return value


rng = np.random.default_rng(2026)
result = minimize(loss, x0=np.pi * rng.standard_normal(6), method="COBYLA", options={"maxiter": 200})
df = pd.DataFrame(history)
df.to_csv(OUTPUTS / "alt_task4_history.csv", index=False)

for _, row in df.iloc[::20].iterrows():
    print(f"  evaluation {int(row.evaluation):>3}:  loss = {row.loss:.4f}")
print(f"\nFinal loss {result.fun:.5f} after {len(df)} evaluations in {df.time_s.iloc[-1]:.2f} s")
for x, y in zip(images, labels):
    p = predict(result.x, x)
    print(f"  image {x}  label {y}  P(bar) = {p:.3f}  ->  {'correct' if (p > 0.5) == bool(y) else 'wrong'}")

fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].plot(df.evaluation, df.loss); ax[0].set(title="Loss per evaluation (COBYLA)", xlabel="Evaluation", ylabel="Loss")
ax[1].plot(df.evaluation, df.time_s); ax[1].set(title="Cumulative time", xlabel="Evaluation", ylabel="Seconds")
for a in ax: a.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUTPUTS / "alt_task4_plots.png", dpi=150)
print("Saved:", OUTPUTS / "alt_task4_plots.png")
