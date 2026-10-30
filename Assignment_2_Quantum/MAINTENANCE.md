# MAINTENANCE GUIDE — MSE802 Assessment 2 (Quantum Project)

Group: **Anish Shrestha** (270889991) and **Sandhya Tiwari** (270888992)
Last updated: 31 October 2026

This guide explains how to set up, run, test, update and fix the project.

---

## 1. Folder map

```
Assignment_2_Quantum/
├── common/quokka_helper.py          shared code: clean QASM, call Quokka, fallback, counts, plots
├── Task_1_Bell_State/               Cirq Bell state
├── Task_2_Qiskit_QASM/              Qiskit circuit + custom QASM (custom_half_adder.qasm)
├── Task_3_Quantum_TicTacToe/        completed game + original
├── Task_4_Quantum_ML/               modified ML notebook + original
├── Alternative_Code/                second solution for each task (+ outputs/)
├── Report/                          Assignment2.docx / Assignment2.pdf
├── Colab_Run_All_Tasks.ipynb        run everything in Google Colab
├── run_project.py                   runner: menu / all / one task / alt / status
├── run_project.bat, run_all.bat     Windows launchers (set up .venv first time)
├── run_project.sh                   macOS / Linux launcher
├── outputs_html/                    created by the runner: one web page per task
├── requirements.txt                 exact package versions
├── quokka_config.json               which Quokka to use (default quokka1)
└── MAINTENANCE.md                   this file
```

Each task folder has a `results/` folder with the evidence: JSON (raw counts + source + time), CSV tables and PNG figures.

## 2. First-time set-up (Windows + VS Code)

1. Install **Python 3.12 or newer** from python.org and tick **"Add python.exe to PATH"**.
2. Double-click **`run_project.bat`** (menu) or **`run_all.bat`** (Tasks 1–4 together). The first run creates `.venv`, installs the packages and writes `.venv\installed.flag`; later runs start straight away. Delete that flag file to force a re-install after changing `requirements.txt`.
3. In VS Code: *File → Open Folder* → `Assignment_2_Quantum`, open a notebook, click **Select Kernel** and pick `.venv` (or "Python 3 (MSE802)").

Manual alternative:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

## 3. How the Quokka connection works

* Address: `http://quokka1.quokkacomputing.com/qsim/qasm` (from the course notebook `quokka_access.ipynb`).
* Request: `POST` JSON `{"script": <OpenQASM 2.0>, "count": <shots>}`.
* Reply: `{"error": "no error", "error_code": 0, "result": {"<register>": [[c0, c1, ...], ...]}}`, one list per shot.
* `clean_qasm()` removes `include "qelib1.inc";`, comments and `barrier` lines, because Quokka does not have the library.
* `to_quokka_gates()` rewrites any gate Quokka does not support (s, t, ccx, ...) into its documented QASM gate set h, x, y, z, rx, ry, rz, cx, swap, and writes angles as numbers. Source: the official *Quokka docs* Colab notebook.
* **Shots:** every task uses **1000** (`SHOTS = 1000` at the top of each notebook).

**Test the connection on its own:**
```bat
.venv\Scripts\activate
python common\quokka_helper.py
```
It prints `Quokka status: online` or the reason it is offline.

## 4. Offline fallback (important for honesty in the report)

If Quokka cannot be reached, `run_qasm()` runs the **same QASM** on Qiskit Aer and sets
`source = "LOCAL SIMULATOR (Qiskit Aer) - Quokka was not reachable"`. Every notebook prints the source, and every JSON file stores it.
**Never report a LOCAL SIMULATOR result as a Quokka result.** To forbid the fallback, call `run_qasm(..., allow_fallback=False)`.

On 31 October 2026 the Quokka endpoint replied *"endpoint is offline (ERR_NGROK_3200)"*, so the first saved results are local-simulator results. When Quokka is online again, run `run_all.bat` (or `python run_project.py all`, or the Colab notebook). The results are overwritten with Quokka data and the source label changes to `QUOKKA DEVICE`.

## 5. Common problems and fixes

| Problem | Likely cause | Fix |
|---|---|---|
| `python is not recognized` | Python not on PATH | Reinstall Python and tick "Add to PATH", or use `py` instead of `python` |
| `ModuleNotFoundError: cirq` (or qiskit) | wrong kernel in VS Code | Select the `.venv` kernel (top-right of the notebook) |
| `ModuleNotFoundError: quokka_helper` | notebook opened from another folder | Open the notebook from inside its task folder; the code adds `../common` to the path |
| `Quokka endpoint is offline (ERR_NGROK_3200)` | the Quokka server is switched off | Wait and re-run; results meanwhile are labelled LOCAL SIMULATOR |
| `Quokka error: ...` (error 7 = INVALID_QASM) | a gate Quokka does not support | `to_quokka_gates()` already rewrites gates into Quokka's set (h, x, y, z, rx, ry, rz, cx, swap); check the printed script in the JSON file |
| `requests.exceptions.ConnectTimeout` | no internet or firewall | Check the internet connection or campus proxy; `REQUEST_TIMEOUT` is in `quokka_helper.py` |
| Circuit drawings missing / `pylatexenc` error | drawer dependency missing | `pip install pylatexenc` |
| Task 3 buttons do not appear | ipywidgets not enabled | `pip install ipywidgets` and restart VS Code; the recorded games (Section 6) work without buttons |
| Task 4 is slow on Quokka | 900 network requests (100 iterations × 9 circuits) | Normal (a few minutes); lower `MAXITER` for a quick test |
| the runner stops with a Python traceback | an error inside a notebook | the traceback names the cell; open the notebook and run it cell by cell |
| Colab: `ModuleNotFoundError: quokka_helper` | the Colab bootstrap cell was skipped | run the first code cell ("Google Colab bootstrap") before the others |
| Colab: Task 3 buttons do not react | widget manager not enabled | the bootstrap cell enables it; re-run it, or use the recorded games / `Alternative_Code` text game |

## 6. How to change things safely

| I want to... | Change this |
|---|---|
| use a different number of shots | `SHOTS = 1000` at the top of each notebook |
| change the Quokka address | `"quokka_name"` in `quokka_config.json`, or the `QUOKKA_NAME` / `QUOKKA_URL` environment variable (no code change) |
| change the size of an X/O move in the game | `ROTATION = math.pi / 4` in the Task 3 notebook |
| run more or fewer ML iterations | `MAXITER = 100` in the Task 4 notebook |
| get different random results in Task 4 | `SEED = 2026` in the Task 4 notebook |
| edit our custom circuit | `Task_2_Qiskit_QASM/custom_half_adder.qasm` (then re-run Task 2) |

## 7. Quick test checklist (after any change)

- [ ] `python common\quokka_helper.py` prints a status
- [ ] Task 1: only `00` and `11` appear, each about 500 of 1000
- [ ] Task 2A: only `01` and `10` appear; Task 2B: only `0000`, `1001`, `1010`, `0111`, about 250 each
- [ ] Task 3: Game 3 tile 4 has P(X) = 0.00; Game 4 tile 8 has P(X) = 1.00
- [ ] Task 4: "Our simulator" and "Qiskit" values printed in Section 8 are equal
- [ ] Every result shows its source (QUOKKA DEVICE or LOCAL SIMULATOR)

## 8. Version history

| Date | Change |
|---|---|
| 31 Oct 2026 | Project structure, shared helper, notebooks for Tasks 1–4, custom QASM, maintenance guide |
| 31 Oct 2026 | Runner (run_project.py/.bat/.sh), alternative code, Colab notebook, GitHub README |
| 31 Oct 2026 | Quokka gate-set translation, configurable Quokka address, Task 3/4 Word documents, verified references |
