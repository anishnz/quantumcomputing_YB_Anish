"""
quokka_helper.py
================
MSE802 Assessment 2 - shared helper used by Tasks 1, 2 and 4.
Group: Anish Shrestha and Sandhya Tiwari.

What this file does (in simple words)
-------------------------------------
1. Cleans an OpenQASM 2.0 script so the Quokka device accepts it
   (Quokka does not have the "qelib1.inc" library, and it does not like
   comment lines that Cirq adds).
2. Sends the script to the Quokka device with a chosen number of shots
   (default 1000), using the same request format as the course notebook
   quokka_access.ipynb.
3. If Quokka cannot be reached (offline, no internet, error reply), it runs
   the SAME QASM script on a local simulator (Qiskit Aer) instead, and labels
   the result "LOCAL SIMULATOR" so it is never mistaken for Quokka data.
4. Converts the raw shot list into counts, e.g. {'00': 503, '11': 497}.
5. Saves every run (script, shots, counts, source, time) as JSON evidence.

Bit-string convention used everywhere in this project
-----------------------------------------------------
Counts keys are written like Qiskit does: the LEFT-most character is the
HIGHEST classical bit.  For 2 bits the key "10" means c[1]=1 and c[0]=0.
"""

# ---------------------------------------------------------------- imports
import json                         # read Quokka's JSON reply and save results
import time                         # measure how long each run takes
from collections import Counter     # count how often each bit-string appears
from datetime import datetime       # time stamp for the evidence files
from pathlib import Path            # safe file paths on Windows and Linux

import requests                     # HTTP POST to the Quokka device
import urllib3                      # silence the warning caused by verify=False (as in the Quokka docs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The Quokka address given in the course notebook (Week 4 / Week 7 quokka_access.ipynb)
QUOKKA_URL = "http://quokka1.quokkacomputing.com/qsim/qasm"

DEFAULT_SHOTS = 1000                # the group agreed on 1000 shots for every circuit
REQUEST_TIMEOUT = 120               # seconds to wait for Quokka before giving up

LOCAL_SEED = 802                    # seed for the local simulator, so offline results can be repeated exactly

import numpy as _np                 # only used to create the sequence of simulator seeds
_SEEDS = _np.random.default_rng(LOCAL_SEED)

SOURCE_QUOKKA = "QUOKKA DEVICE"
SOURCE_LOCAL = "LOCAL SIMULATOR (Qiskit Aer) - Quokka was not reachable"


# ------------------------------------------------------- 1. clean the QASM
def clean_qasm(qasm_text: str) -> str:
    """Return a Quokka-friendly copy of an OpenQASM 2.0 script.

    - removes the line  include "qelib1.inc";   (library not installed on Quokka)
    - removes comment lines that start with //  (Cirq adds these)
    - removes empty lines and extra spaces
    The course notebook removed the include line by cutting characters
    (code[:14] + code[36:]); removing it by text is safer because it still
    works if the header length changes.
    """
    kept = []
    for line in qasm_text.splitlines():
        line = line.strip()                       # remove spaces/indentation
        if not line:                              # skip blank lines
            continue
        if line.startswith("//"):                 # skip comments
            continue
        if line.startswith("include"):            # skip include "qelib1.inc";
            continue
        if line.startswith("barrier"):            # barriers only affect drawings, not results
            continue
        if "//" in line:                          # remove a comment written at the end of a line
            line = line.split("//")[0].rstrip()
        kept.append(line)
    return "\n".join(kept) + "\n"


# ---------------------------------------- 1b. only use gates Quokka supports
# From the official "Quokka docs" notebook (QASM Support table): the Quokka simulator
# understands h, x, y, z, rx, ry, rz, cx, swap, cphase, U (and lerr for error simulation).
# It does NOT list s, t, tdg, ccx (Toffoli), sdg, cz, ... so those must be rewritten.
QUOKKA_GATES = {"h", "x", "y", "z", "rx", "ry", "rz", "cx", "swap"}
_NOT_GATES = {"measure", "barrier"}                  # instructions that are not gates


def to_quokka_gates(qasm_text: str) -> str:
    """Rewrite a circuit so it only uses gates from Quokka's QASM table.

    If the script already uses only supported gates it is returned unchanged
    (so register names such as Cirq's 'm_c' are kept). Otherwise Qiskit's
    transpiler rewrites it, e.g. S -> RZ(pi/2), T -> RZ(pi/4) and the Toffoli
    -> 6 CNOTs + H + RZ gates. RZ differs from S/T only by a global phase,
    which can never change a measurement result.
    """
    import qiskit.qasm2
    from qiskit import transpile

    body = clean_qasm(qasm_text).replace("OPENQASM 2.0;\n", "")
    circuit = qiskit.qasm2.loads('OPENQASM 2.0;\ninclude "qelib1.inc";\n' + body)
    used = set(circuit.count_ops()) - _NOT_GATES
    if used <= QUOKKA_GATES:                         # nothing to rewrite
        return _numeric_angles(clean_qasm(qasm_text))
    rewritten = transpile(circuit, basis_gates=sorted(QUOKKA_GATES), optimization_level=0)
    return _numeric_angles(clean_qasm(qiskit.qasm2.dumps(rewritten)))


def _numeric_angles(qasm_text: str) -> str:
    """Write angles such as rz(pi/2) as plain numbers, e.g. rz(1.5707963267948966).

    The Quokka documentation only shows numeric angles, so this avoids relying
    on the simulator understanding the symbol 'pi'.
    """
    import math
    import re

    def number(match):
        expr = match.group(1)
        if "pi" not in expr:
            return match.group(0)
        value = eval(expr, {"__builtins__": {}}, {"pi": math.pi})   # only 'pi' and arithmetic allowed
        return f"({value!r})"

    return re.sub(r"\(([0-9pi\.\*/\+\- eE]+)\)", number, qasm_text)


# ------------------------------------------------- 2. send to Quokka device
def run_on_quokka(qasm_text: str, shots: int = DEFAULT_SHOTS) -> dict:
    """Send one script to Quokka. Returns the decoded JSON reply.

    Request format (from the course notebook):
        POST QUOKKA_URL   json = {"script": <qasm>, "count": <shots>}
    Reply format:
        {"error": "no error", "error_code": 0,
         "result": {"<creg name>": [[bit0, bit1, ...], ...one list per shot]}}
    Raises RuntimeError if the device is offline or replies with an error.
    """
    payload = {"script": to_quokka_gates(qasm_text), "count": int(shots)}
    # verify=False exactly as in the official Quokka notebooks
    reply = requests.post(QUOKKA_URL, json=payload, timeout=REQUEST_TIMEOUT, verify=False)
    if reply.status_code != 200:                  # e.g. 404 when the endpoint is offline
        if "ERR_NGROK_3200" in reply.text:        # Quokka's tunnel reports this when the device is off
            raise RuntimeError("Quokka endpoint is offline (HTTP 404, ERR_NGROK_3200)")
        raise RuntimeError(f"Quokka HTTP {reply.status_code}")
    data = json.loads(reply.content)              # turn the text reply into a dict
    if data.get("error_code", 1) != 0:            # Quokka reports its own errors here
        raise RuntimeError(f"Quokka error: {data.get('error')}")
    return data


# ------------------------------------------ 3. local fallback (same script)
def run_locally(qasm_text: str, shots: int = DEFAULT_SHOTS) -> list:
    """Run the same QASM on Qiskit Aer and return shots in Quokka's format.

    Each shot is a list [c0, c1, ...] (lowest bit first) - exactly the shape
    Quokka returns - so the rest of the code does not care where it came from.
    """
    import qiskit.qasm2                              # load OpenQASM 2.0 text
    from qiskit import transpile                     # map gates to the simulator
    from qiskit_aer import AerSimulator              # fast local simulator

    script = to_quokka_gates(qasm_text)              # run exactly what Quokka would receive
    full = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n' + script.replace("OPENQASM 2.0;\n", "")
    circuit = qiskit.qasm2.loads(full)               # build a QuantumCircuit from text
    seed = int(_SEEDS.integers(0, 2**31 - 1))        # next seed from a fixed sequence -> repeatable results
    sim = AerSimulator(seed_simulator=seed)
    job = sim.run(transpile(circuit, sim), shots=shots, memory=True)
    memory = job.result().get_memory()               # one bit-string per shot, e.g. "10"
    n = circuit.num_clbits
    # Qiskit strings are highest bit first, so reverse them to get [c0, c1, ...]
    return [[int(b) for b in reversed(m.replace(" ", ""))][:n] for m in memory]


# -------------------------------------------------- 4. shots -> counts
def shots_to_counts(shots: list) -> dict:
    """Turn [[c0, c1], [c0, c1], ...] into {'c1c0': count} (Qiskit order)."""
    keys = ["".join(str(b) for b in reversed(s)) for s in shots]
    return dict(sorted(Counter(keys).items()))


def counts_to_probs(counts: dict) -> dict:
    """Divide each count by the total to get measured probabilities."""
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}


def total_variation_distance(p: dict, q: dict) -> float:
    """Half the sum of absolute differences: 0 = identical, 1 = completely different."""
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


# ------------------------------------------- 5. one call does everything
def run_qasm(qasm_text: str, shots: int = DEFAULT_SHOTS, label: str = "run",
             save_dir: str | Path | None = None, allow_fallback: bool = True) -> dict:
    """Try Quokka first, fall back to the local simulator, save evidence.

    Returns a dict with: label, source, shots_requested, counts, probs,
    seconds, timestamp, qasm, error (why Quokka failed, if it did).
    """
    start = time.perf_counter()                    # start the stopwatch
    error = None
    try:
        data = run_on_quokka(qasm_text, shots)
        shot_list = list(data["result"].values())[0]   # first (only) classical register
        source = SOURCE_QUOKKA
    except Exception as exc:                       # offline, timeout, bad reply ...
        if not allow_fallback:
            raise
        error = str(exc)[:200]
        shot_list = run_locally(qasm_text, shots)
        source = SOURCE_LOCAL
    seconds = time.perf_counter() - start          # stop the stopwatch

    counts = shots_to_counts(shot_list)
    record = {
        "label": label,
        "source": source,
        "shots_requested": shots,
        "shots_received": len(shot_list),
        "counts": counts,
        "probs": counts_to_probs(counts),
        "seconds": round(seconds, 4),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "qasm": to_quokka_gates(qasm_text),          # the exact script sent (Quokka gate set)
        "quokka_error": error,
    }
    if save_dir is not None:                       # keep evidence for the report
        folder = Path(save_dir)
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / f"{label}.json", "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2)
    return record


def quokka_status() -> str:
    """Quick connection test: returns 'online' or a short reason it is offline."""
    try:
        run_on_quokka("OPENQASM 2.0;\nqreg q[1];\ncreg c[1];\nmeasure q[0] -> c[0];\n", 1)
        return "online"
    except Exception as exc:
        return f"offline ({str(exc)[:90]})"


# ------------------------------------------------------ 6. plotting helper
def plot_comparison(series: dict, title: str, path=None, ylabel="Probability"):
    """Grouped bar chart, e.g. series = {'Theory': {...}, 'Measured': {...}}."""
    import matplotlib.pyplot as plt
    import numpy as np

    keys = sorted(set().union(*[set(s) for s in series.values()]))
    x = np.arange(len(keys))
    width = 0.8 / len(series)
    colours = ["#3b6ea5", "#e07a3f", "#5a9e6f", "#8e6bb8"]
    fig, ax = plt.subplots(figsize=(7, 4))
    for i, (name, values) in enumerate(series.items()):
        heights = [values.get(k, 0) for k in keys]
        bars = ax.bar(x + i * width - 0.4 + width / 2, heights, width,
                      label=name, color=colours[i % len(colours)])
        ax.bar_label(bars, fmt="%.3f", fontsize=8, padding=2)
    ax.set_xticks(x, keys)
    ax.set_xlabel("Measured bit-string (highest bit on the left)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_ylim(0, max(1.05 * max(max(v.values(), default=0) for v in series.values()), 0.1) + 0.08)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=200)
    return fig


if __name__ == "__main__":
    # Running this file directly gives a quick connection test.
    print("Quokka status:", quokka_status())
