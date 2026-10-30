# MSE802 Quantum Computing — Assignment 2: Quantum Project

**Yoobee College of Creative Innovation · Master of Software Engineering (Level 8)**
**Group:** Anish Shrestha (270889991) and Sandhya Tiwari (270888992) · **Lecturer:** Dr Helena Bahrami

This repository holds the code, results and report for Assessment 2. Each task has its own folder, notebook and `results/` folder:

| Task | What it does | Notebook | Open in Colab |
|---|---|---|---|
| **Task 1** | Bell state (\|00⟩+\|11⟩)/√2 with **Cirq**, run on **Quokka** (1000 shots) | [`Task1_Bell_State_Cirq_Quokka.ipynb`](Assignment_2_Quantum/Task_1_Bell_State/Task1_Bell_State_Cirq_Quokka.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anishnz/quantumcomputing_YB_Anish/blob/main/Assignment_2_Quantum/Task_1_Bell_State/Task1_Bell_State_Cirq_Quokka.ipynb) |
| **Task 2** | Given H–X–C circuit in **Qiskit** + our own **QASM** circuit (quantum half adder) | [`Task2_Qiskit_Circuits_and_QASM.ipynb`](Assignment_2_Quantum/Task_2_Qiskit_QASM/Task2_Qiskit_Circuits_and_QASM.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anishnz/quantumcomputing_YB_Anish/blob/main/Assignment_2_Quantum/Task_2_Qiskit_QASM/Task2_Qiskit_Circuits_and_QASM.ipynb) |
| **Task 3** | Completed **quantum tic-tac-toe** game + 4 recorded games | [`Task3_Quantum_TicTacToe_Completed.ipynb`](Assignment_2_Quantum/Task_3_Quantum_TicTacToe/Task3_Quantum_TicTacToe_Completed.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anishnz/quantumcomputing_YB_Anish/blob/main/Assignment_2_Quantum/Task_3_Quantum_TicTacToe/Task3_Quantum_TicTacToe_Completed.ipynb) |
| **Task 4** | **Quantum ML** classifier: iteration logging, 2 graphs, quantum vs local comparison | [`Task4_Quantum_ML_Modified.ipynb`](Assignment_2_Quantum/Task_4_Quantum_ML/Task4_Quantum_ML_Modified.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anishnz/quantumcomputing_YB_Anish/blob/main/Assignment_2_Quantum/Task_4_Quantum_ML/Task4_Quantum_ML_Modified.ipynb) |
| **All tasks** | Runs Tasks 1–4 together, shows results, runs the alternative code | [`Colab_Run_All_Tasks.ipynb`](Assignment_2_Quantum/Colab_Run_All_Tasks.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anishnz/quantumcomputing_YB_Anish/blob/main/Assignment_2_Quantum/Colab_Run_All_Tasks.ipynb) |

📄 **Report:** [`Assignment_2_Quantum/Report/Assignment2.pdf`](Assignment_2_Quantum/Report/Assignment2.pdf) (Word version: `Assignment2.docx`) · Task Word documents: [Task 3](Assignment_2_Quantum/Task_3_Quantum_TicTacToe/Task3_Report_Quantum_TicTacToe.pdf), [Task 4](Assignment_2_Quantum/Task_4_Quantum_ML/Task4_Report_Quantum_ML.pdf) · 📦 Submission ZIP: [`MSE802_Assignment2_Shrestha_Tiwari.zip`](MSE802_Assignment2_Shrestha_Tiwari.zip)

---

## 1. Quick start — choose ONE way

### Option A — Google Colab (nothing to install) ⭐ easiest
1. Click the **Open in Colab** badge in the **All tasks** row above.
2. In Colab, click **Runtime → Run all**.
3. Wait about 4–5 minutes. The notebook downloads this repository, installs Cirq and Qiskit, runs **Tasks 1–4 together**, shows every result and chart, and runs the alternative code.
4. To keep your own copy, click **Copy to Drive** — it is saved in *My Drive → Colab Notebooks* as a new Colab project.

✅ Tested in Colab on 31 October 2026: all four tasks finished without errors (Task 4 takes about 160 s on Colab's free CPU).

To run **one task**, click that task's badge, then **Runtime → Run all**. Its first code cell downloads the project automatically.

> You can also connect GitHub inside Colab: **File → Open notebook → GitHub tab**, type `anishnz/quantumcomputing_YB_Anish`, and pick any notebook.

### Option B — Windows, one click
1. Install **Python 3.12 or newer** from [python.org](https://www.python.org/downloads/) and tick **"Add python.exe to PATH"**.
2. Download this repository: green **Code** button → **Download ZIP** (then unzip), or:
   ```bat
   git clone https://github.com/anishnz/quantumcomputing_YB_Anish.git
   ```
3. Open the `Assignment_2_Quantum` folder and **double-click `run_project.bat`**.
   The first run creates a virtual environment `.venv` and installs the packages (a few minutes). Then a menu appears:
   ```
   1  Task 1 - Bell state (Cirq)
   2  Task 2 - Qiskit circuit + custom QASM
   3  Task 3 - Quantum tic-tac-toe
   4  Task 4 - Quantum machine learning
   A  Run Tasks 1-4 together
   L  Run the alternative code
   S  Test the Quokka connection
   Q  Quit
   ```
   **`run_all.bat`** runs Tasks 1–4 together without the menu.

### Option C — Any computer, from a terminal (Windows / macOS / Linux)
```bash
cd quantumcomputing_YB_Anish/Assignment_2_Quantum
python -m venv .venv
.venv\Scripts\activate            # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt

python run_project.py             # menu
python run_project.py all         # Tasks 1, 2, 3 and 4 together
python run_project.py 1           # only Task 1   (also 2, 3, 4)
python run_project.py alt         # the alternative code for all tasks
python run_project.py status      # test the Quokka connection only
```
On macOS/Linux you can also use `./run_project.sh all`.

### Option D — VS Code / Jupyter, cell by cell
1. Do the `pip install` step from Option C.
2. In VS Code: **File → Open Folder** → `Assignment_2_Quantum`, open a task notebook, click **Select Kernel** → choose `.venv`.
3. Click **Run All**. (Or run `jupyter notebook` and open the notebooks in the browser.)

---

## 2. Where to see the output

| Where | What you see |
|---|---|
| **Terminal** | after each task, `run_project.py` prints the key results (counts, game win chances, Task 4 comparison) |
| **Inside each notebook** | circuit diagrams, tables, histograms and graphs are saved in the executed `.ipynb` |
| **`outputs_html/`** | one web page per task (`Task_1_Bell_State.html` …), double-click to open in any browser |
| **`<Task>/results/`** | evidence files: raw counts + source (JSON), tables (CSV), charts (PNG) |
| **`Alternative_Code/outputs/`** | outputs of the alternative scripts |

Example terminal output of `python run_project.py all`:
```
Quokka device: online                (or: offline -> results labelled LOCAL SIMULATOR)
RUNNING Task 1 - Bell state (Cirq)
  counts (1000 shots): {'00': 508, '11': 492}   expected: only 00 and 11
RUNNING Task 2 - Qiskit circuit + custom QASM
  2A H-X-CNOT counts: {'01': 492, '10': 508}   expected: only 01 and 10
  2B half adder counts: {'0000': 250, '0111': 244, '1001': 247, '1010': 259}
RUNNING Task 3 - Quantum tic-tac-toe
  game2_diagonals  X wins  705/1000   O wins  210/1000
RUNNING Task 4 - Quantum machine learning
  Quantum circuit (1000 shots)   0.56 s/iter   final loss 0.0   all 4 images 1.0
  Local-A: same circuit, exact   0.0011 s/iter final loss 0.0003 all 4 images 1.0
ALL FOUR TASKS FINISHED. Open outputs_html/ to see every result.
```

---

## 3. The Quokka device (important)

* Circuits are sent to Quokka as OpenQASM 2.0: `POST http://quokka1.quokkacomputing.com/qsim/qasm` with `{"script": ..., "count": 1000}` (same as the course notebook `quokka_access.ipynb`).
* Every task uses **1000 shots** (`SHOTS = 1000` at the top of each notebook).
* If Quokka is **offline**, the same QASM runs on the Qiskit Aer simulator, and every result is labelled **`LOCAL SIMULATOR`** in the output and JSON files, so it is never presented as Quokka data.
* On 31 October 2026 the Quokka endpoint was offline (`ERR_NGROK_3200`), so the saved results in this repository are labelled LOCAL SIMULATOR. **Re-run when Quokka is online** (any option above) and the results are replaced with device results labelled `QUOKKA DEVICE`.
* **Why it fails although the Quokka notebooks are public:** the notebooks are only instructions. The simulator is a separate server reached through an ngrok tunnel, and `ERR_NGROK_3200` means that server is switched off on Quokka's side. The official docs use **no login or API key**, so signing in would not change this.
* **Gate set:** the Quokka docs list `h, x, y, z, rx, ry, rz, cx, swap, cphase, U`. `quokka_helper.to_quokka_gates()` automatically rewrites anything else (e.g. `s`, `ccx`) before sending.
* **Using a different Quokka** (e.g. one your lecturer gives you): edit `Assignment_2_Quantum/quokka_config.json` → `"quokka_name": "quokka7"`, or set the environment variable `QUOKKA_NAME`. No code changes are needed.
* Check the connection at any time: `python run_project.py status`, or open http://quokka1.quokkacomputing.com/qsim/qasm in a browser (an `ERR_NGROK_3200` page means offline).

---

## 4. Repository structure

```
quantumcomputing_YB_Anish/
├── README.md                                  <- you are here
└── Assignment_2_Quantum/
    ├── Task_1_Bell_State/
    │   ├── Task1_Bell_State_Cirq_Quokka.ipynb
    │   └── results/                           counts JSON, table CSV, histogram, QASM
    ├── Task_2_Qiskit_QASM/
    │   ├── Task2_Qiskit_Circuits_and_QASM.ipynb
    │   ├── custom_half_adder.qasm             our own QASM circuit
    │   └── results/
    ├── Task_3_Quantum_TicTacToe/
    │   ├── Task3_Quantum_TicTacToe_Completed.ipynb   completed + commented game
    │   ├── Original_Quantum_Tic_Tac_Toe__AS2.ipynb   supplied version (unchanged)
    │   ├── Task3_Report_Quantum_TicTacToe.docx/.pdf  Task 3 Word document (required)
    │   └── results/                           4 game circuits, summaries, tile chances
    ├── Task_4_Quantum_ML/
    │   ├── Task4_Quantum_ML_Modified.ipynb    modified notebook (required .ipynb)
    │   ├── Original_Quantum_ML_AS2.ipynb      supplied version (unchanged)
    │   ├── Task4_Report_Quantum_ML.docx/.pdf  Task 4 Word document (required)
    │   └── results/                           iteration logs, 2 graphs, comparison
    ├── Alternative_Code/                      a second solution for every task
    │   ├── Task_1_Alt_Qiskit/                 Bell state in Qiskit
    │   ├── Task_2_Alt_Cirq/                   Task 2 circuits in Cirq
    │   ├── Task_3_Alt_Text_Game/              terminal tic-tac-toe (try --demo)
    │   ├── Task_4_Alt_Statevector/            exact classifier + COBYLA optimiser
    │   └── outputs/
    ├── common/quokka_helper.py                Quokka call, labelled fallback, counts, charts
    ├── Colab_Run_All_Tasks.ipynb              whole project in Google Colab
    ├── run_project.py                         runner (menu / all / one task / alt)
    ├── run_project.bat · run_all.bat · run_project.sh
    ├── quokka_config.json                     which Quokka to use (default quokka1)
    ├── requirements.txt                       exact package versions
    ├── MAINTENANCE.md                         troubleshooting and safe changes
    └── Report/Assignment2.docx · Assignment2.pdf
```

---

## 5. Alternative code

Each alternative solves the same task in a different way, as an independent check. Run all of them with `python run_project.py alt`, or one at a time:

```bash
python Alternative_Code/Task_1_Alt_Qiskit/task1_bell_state_qiskit.py
python Alternative_Code/Task_2_Alt_Cirq/task2_circuits_cirq.py
python Alternative_Code/Task_3_Alt_Text_Game/task3_tictactoe_terminal.py          # play: X 4, O 2, NOT 4, SWAP 0 8, PROB, MEASURE
python Alternative_Code/Task_3_Alt_Text_Game/task3_tictactoe_terminal.py --demo   # automatic demo game
python Alternative_Code/Task_4_Alt_Statevector/task4_classifier_statevector.py
```

---

## 6. Requirements

Python 3.12+ and the packages in [`requirements.txt`](Assignment_2_Quantum/requirements.txt): cirq-core 1.7, qiskit 2.6, qiskit-aer 0.18, numpy, scipy, pandas, matplotlib, pylatexenc, requests, ipywidgets, notebook, nbconvert, ipykernel.

## 7. Problems?

See [`MAINTENANCE.md`](Assignment_2_Quantum/MAINTENANCE.md) for common errors (Python not found, wrong VS Code kernel, Quokka offline, missing widgets) and how to change shots, iterations or the Quokka address safely.

---
*MSE802 Quantum Computing — Assessment 2 (Group Project), 2026. Sources are cited in APA 7th style in the report.*
