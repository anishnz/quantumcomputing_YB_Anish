"""
run_project.py - one program to run and check MSE802 Assessment 2 (Tasks 1-4).

How to use (from the Assignment_2_Quantum folder):
    python run_project.py            -> menu: choose a task
    python run_project.py all        -> run Tasks 1, 2, 3 and 4 together
    python run_project.py 1          -> run only Task 1   (also 2, 3, 4)
    python run_project.py alt        -> run the alternative code for all tasks
    python run_project.py status     -> only test the Quokka connection

What it does for each task:
    1. executes the task notebook (the outputs are saved inside the .ipynb)
    2. exports an HTML copy to outputs_html/  -> open it in any web browser
    3. prints a short summary of the results in this terminal
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent                       # the Assignment_2_Quantum folder
sys.path.insert(0, str(ROOT / "common"))
HTML_DIR = ROOT / "outputs_html"

TASKS = {
    "1": ("Task 1 - Bell state (Cirq)", "Task_1_Bell_State", "Task1_Bell_State_Cirq_Quokka.ipynb"),
    "2": ("Task 2 - Qiskit circuit + custom QASM", "Task_2_Qiskit_QASM", "Task2_Qiskit_Circuits_and_QASM.ipynb"),
    "3": ("Task 3 - Quantum tic-tac-toe", "Task_3_Quantum_TicTacToe", "Task3_Quantum_TicTacToe_Completed.ipynb"),
    "4": ("Task 4 - Quantum machine learning", "Task_4_Quantum_ML", "Task4_Quantum_ML_Modified.ipynb"),
}
ALTERNATIVES = [
    "Alternative_Code/Task_1_Alt_Qiskit/task1_bell_state_qiskit.py",
    "Alternative_Code/Task_2_Alt_Cirq/task2_circuits_cirq.py",
    "Alternative_Code/Task_3_Alt_Text_Game/task3_tictactoe_terminal.py --demo",
    "Alternative_Code/Task_4_Alt_Statevector/task4_classifier_statevector.py",
]


def line(char="="):
    print(char * 72)


def quokka_status():
    import quokka_helper as qh                               # imported here so 'status' is quick
    status = qh.quokka_status()
    print(f"Quokka device {qh.QUOKKA_URL}: {status}")
    if status != "online":
        print("  -> circuits will run on the local simulator and be labelled LOCAL SIMULATOR")


KERNEL = "mse802-project"          # Jupyter kernel that uses THIS Python (same packages as the runner)
PACKAGES = {"cirq": "cirq-core", "qiskit": "qiskit", "qiskit_aer": "qiskit-aer", "pylatexenc": "pylatexenc",
            "ipykernel": "ipykernel", "nbconvert": "nbconvert", "ipywidgets": "ipywidgets"}
_ENV_READY = False


def ensure_environment():
    """Install missing packages into this Python and register a kernel that points to it.

    Without this, a notebook could be executed by a different Python (for example in Google
    Colab), which would not have Cirq/Qiskit installed and would fail with ModuleNotFoundError.
    """
    global _ENV_READY
    if _ENV_READY:
        return
    import importlib.util
    missing = [pip_name for module, pip_name in PACKAGES.items() if importlib.util.find_spec(module) is None]
    if missing:
        print("Installing missing packages:", ", ".join(missing))
        subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + missing, check=True)
    from ipykernel.kernelspec import install                 # writes kernel.json -> [sys.executable, ...]
    install(user=True, kernel_name=KERNEL, display_name="Python (MSE802 project)")
    _ENV_READY = True


def run_notebook(task_id):
    """Execute one notebook in its own folder, then export it to HTML."""
    ensure_environment()
    import nbformat
    from nbconvert import HTMLExporter
    from nbconvert.preprocessors import ExecutePreprocessor

    title, folder, name = TASKS[task_id]
    path = ROOT / folder / name
    line(); print(f"RUNNING {title}\n  notebook: {folder}/{name}"); line("-")
    nb = nbformat.read(path, as_version=4)
    start = time.perf_counter()
    ExecutePreprocessor(timeout=3600, kernel_name=KERNEL).preprocess(nb, {"metadata": {"path": str(path.parent)}})
    nbformat.write(nb, path)                                 # keep the outputs inside the notebook
    HTML_DIR.mkdir(exist_ok=True)
    html, _ = HTMLExporter().from_notebook_node(nb)
    html_file = HTML_DIR / f"{folder}.html"
    html_file.write_text(html, encoding="utf-8")
    print(f"  finished in {time.perf_counter() - start:.1f} s")
    print(f"  output saved in the notebook and as HTML: outputs_html/{html_file.name}")
    summarise(task_id)


def _load(folder, file):
    p = ROOT / folder / "results" / file
    return json.loads(p.read_text()) if p.exists() else None


def summarise(task_id):
    """Print the key numbers from the saved results files."""
    print("  RESULTS:")
    if task_id == "1":
        r = _load("Task_1_Bell_State", "task1_bell_quokka.json")
        print(f"    source: {r['source']}\n    counts (1000 shots): {r['counts']}   expected: only 00 and 11, ~500 each")
    elif task_id == "2":
        a = _load("Task_2_Qiskit_QASM", "task2a_both_qubits.json")
        b = _load("Task_2_Qiskit_QASM", "task2b_half_adder.json")
        print(f"    source: {a['source']}")
        print(f"    2A H-X-CNOT counts: {a['counts']}   expected: only 01 and 10")
        print(f"    2B half adder counts: {b['counts']}   expected: 0000, 1001, 1010, 0111 (~250 each)")
    elif task_id == "3":
        import csv
        with open(ROOT / "Task_3_Quantum_TicTacToe" / "results" / "task3_games_summary.csv") as fh:
            for row in csv.DictReader(fh):
                print(f"    {row['name']:<16} X wins {row['X wins /1000']:>4}/1000   O wins {row['O wins /1000']:>4}/1000")
    elif task_id == "4":
        import csv
        with open(ROOT / "Task_4_Quantum_ML" / "results" / "task4_comparison.csv") as fh:
            for row in csv.DictReader(fh):
                print(f"    {row['Version'][:42]:<42} {row['Mean time / iteration (s)']:>9} s/iter   "
                      f"final loss {row['Final loss (monitored)']:>6}   all 4 images {row['All 4 images']}")
        print("    plots: Task_4_Quantum_ML/results/task4_iteration_vs_output.png and ..._vs_time.png")


def run_alternatives():
    ensure_environment()
    for script in ALTERNATIVES:
        line(); print(f"ALTERNATIVE: {script}"); line("-")
        subprocess.run([sys.executable] + script.split(), cwd=ROOT, check=False)
    print("\nAlternative outputs saved in Alternative_Code/outputs/")


def menu():
    while True:
        line()
        print("MSE802 Assessment 2 - Quantum Project")
        line()
        for k, (title, *_rest) in TASKS.items():
            print(f"  {k}  {title}")
        print("  A  Run Tasks 1-4 together\n  L  Run the alternative code\n  S  Test the Quokka connection\n  Q  Quit")
        choice = input("Choose: ").strip().upper()
        if choice == "Q":
            return
        handle(choice)


def handle(choice):
    choice = choice.upper()
    if choice in TASKS:
        quokka_status(); run_notebook(choice)
    elif choice in ("A", "ALL"):
        quokka_status()
        for task_id in TASKS:
            run_notebook(task_id)
        line(); print("ALL FOUR TASKS FINISHED. Open outputs_html/ to see every result."); line()
    elif choice in ("L", "ALT"):
        run_alternatives()
    elif choice in ("S", "STATUS"):
        quokka_status()
    else:
        print("Unknown choice:", choice)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle(sys.argv[1])
    else:
        menu()
