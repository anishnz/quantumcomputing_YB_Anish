"""
compare_laptop_vs_quokka.py
MSE802 Assessment 2 - laptop vs Quokka comparison (asked for by the lecturer).
Runs the SAME circuits (1000 shots, 5 repeats) on the local laptop simulator and on
every Quokka device, then saves a JSON file, a CSV table and two charts.
Run:  python Device_Comparison/compare_laptop_vs_quokka.py
"""
import csv                                                   # write the summary table
import sys                                                   # add ../common to the import path
from pathlib import Path                                     # safe paths on Windows and Linux

HERE = Path(__file__).resolve().parent                       # this folder
sys.path.insert(0, str(HERE.parent / "common"))              # so we can import the helper
import quokka_helper as qh                                   # shared Quokka code
import matplotlib                                            # charts
matplotlib.use("Agg")                                        # draw without a screen
import matplotlib.pyplot as plt

OUT = HERE / "results"                                       # evidence folder
SHOTS, REPEATS = 1000, 5                                     # group standard: 1000 shots

CIRCUITS = {                                                 # name -> QASM file / text
    "task1_bell": (HERE.parent / "Task_1_Bell_State/results/task1_bell_quokka.json"),
    "task2b_half_adder": (HERE.parent / "Task_2_Qiskit_QASM/custom_half_adder.qasm"),
}


def load_qasm(path: Path) -> str:
    """Read a .qasm file, or the 'qasm' field of a saved result JSON."""
    import json
    return json.loads(path.read_text())["qasm"] if path.suffix == ".json" else path.read_text()


rows = []
for name, path in CIRCUITS.items():
    rec = qh.compare_devices(load_qasm(path), SHOTS, REPEATS, label=f"compare_{name}", save_dir=OUT)
    print(f"\n=== {name}  ({rec['timestamp']}) ===")
    for target, r in rec["results"].items():
        print(f"{target:13s}", r)
        rows.append({"circuit": name, "target": target, **{k: r.get(k) for k in
                     ("status", "runs", "mean_seconds", "min_seconds", "max_seconds",
                      "mean_server_ms", "tvd_from_theory")}, "counts_total": r.get("counts_total")})

with open(OUT / "comparison_summary.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

# ---- chart 1: time per 1000-shot run (log scale, laptop vs each device) ----
for metric, title, fname, log in [
        ("mean_seconds", "Mean time per 1000-shot run (wall clock)", "chart_time.png", True),
        ("tvd_from_theory", "Distance from theory (TVD, lower = closer)", "chart_tvd.png", False)]:
    fig, ax = plt.subplots(figsize=(8, 4))
    circuits = list(CIRCUITS)
    targets = [t for t in dict.fromkeys(r["target"] for r in rows) if
               any(r["target"] == t and r["status"] == "ok" for r in rows)]
    width = 0.8 / len(circuits)
    for i, c in enumerate(circuits):
        vals = [next((r[metric] for r in rows if r["circuit"] == c and r["target"] == t), 0) or 0 for t in targets]
        bars = ax.bar([x + i * width - 0.4 + width / 2 for x in range(len(targets))], vals, width, label=c)
        ax.bar_label(bars, fmt="%.3f", fontsize=7, padding=2)
    ax.set_xticks(range(len(targets)), targets)
    if log: ax.set_yscale("log"); ax.set_ylabel("seconds (log scale)")
    else: ax.set_ylabel("TVD")
    ax.set_title(title); ax.legend(); ax.grid(axis="y", alpha=0.3); fig.tight_layout()
    fig.savefig(OUT / fname, dpi=200); plt.close(fig)
print("\nSaved:", sorted(p.name for p in OUT.iterdir()))
