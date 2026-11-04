"""
scaling_laptop_vs_quokka.py
MSE802 Assessment 2 - how does run time grow with the number of qubits?
The same entangling circuit (H on every qubit, a CNOT chain, an RY layer) is run with
2 to 24 qubits, 1000 shots, on this computer (Qiskit Aer) and on one Quokka device.
Run:  python Device_Comparison/scaling_laptop_vs_quokka.py
"""
import csv, json, math, statistics, sys, time                 # standard library
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "common"))
import quokka_helper as qh                                     # shared Quokka code
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = HERE / "results"; OUT.mkdir(exist_ok=True)
SIZES = [2, 4, 8, 12, 16, 20, 22, 24]                          # number of qubits
SHOTS, REPEATS = 1000, 2
DEVICE = next((d for d in qh.QUOKKA_DEVICES if qh.quokka_status([d]).startswith("online")), None)


def circuit(n):
    """H on all qubits, CNOT chain (entangles neighbours), RY(0.3) on all, measure all."""
    lines = ["OPENQASM 2.0;", f"qreg q[{n}];", f"creg c[{n}];"]
    lines += [f"h q[{i}];" for i in range(n)]
    lines += [f"cx q[{i}],q[{i + 1}];" for i in range(n - 1)]
    lines += [f"ry(0.3) q[{i}];" for i in range(n)]
    lines += [f"measure q[{i}] -> c[{i}];" for i in range(n)]
    return "\n".join(lines) + "\n"


rows = []
qh.run_locally(circuit(2), 10)                                 # warm-up (loads Qiskit)
for n in SIZES:
    qasm = circuit(n)
    for target in ["this computer", DEVICE]:
        if target is None:
            continue
        times, server = [], []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            if target == "this computer":
                qh.run_locally(qasm, SHOTS)
            else:
                data = qh.run_on_device(qasm, SHOTS, target)
                server.append(data.get("server_time_ms"))
            times.append(time.perf_counter() - t0)
        row = {"qubits": n, "target": target, "mean_seconds": round(statistics.mean(times), 4),
               "mean_server_ms": round(statistics.mean(server), 2) if server else None,
               "statevector_MB": round(16 * 2 ** n / 1e6, 3)}
        rows.append(row); print(row, flush=True)

with open(OUT / "scaling_summary.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

fig, ax = plt.subplots(figsize=(7.5, 4))
for target, style in [("this computer", "o-"), (DEVICE, "s-")]:
    pts = [r for r in rows if r["target"] == target]
    ax.plot([r["qubits"] for r in pts], [r["mean_seconds"] for r in pts], style, label=f"{target}: total time")
pts = [r for r in rows if r["target"] == DEVICE]
ax.plot([r["qubits"] for r in pts], [r["mean_server_ms"] / 1000 for r in pts], "s--", color="#8e6bb8", label=f"{DEVICE}: time inside the device")
ax.set_yscale("log"); ax.set_xlabel("Number of qubits"); ax.set_ylabel("Seconds per 1000-shot run (log scale)")
ax.set_title("Run time versus circuit size: this computer vs Quokka"); ax.grid(alpha=.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "chart_scaling.png", dpi=200)
json.dump({"device": DEVICE, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S %z"), "rows": rows}, open(OUT / "scaling.json", "w"), indent=1)
print("saved", OUT / "chart_scaling.png")
