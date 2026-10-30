"""
Task 3 - ALTERNATIVE version: quantum tic-tac-toe in the terminal (no buttons, no widgets).

Same rules and same gates as the completed notebook:
  start : H on every tile (50 % X / 50 % O)
  X n   : RY(-pi/4) on tile n   (toward |0> = X)
  O n   : RY(+pi/4) on tile n   (toward |1> = O)
  NOT n : X gate on tile n      (flips ownership; does nothing to an undecided tile)
  SWAP a b : SWAP gate between tiles a and b
  MEASURE  : run the circuit once, show the board and count winning lines
  PROB     : (extra) run 1000 shots and show each tile's chance of becoming X

Run interactively:   python Alternative_Code/Task_3_Alt_Text_Game/task3_tictactoe_terminal.py
Run a demo game:     python Alternative_Code/Task_3_Alt_Text_Game/task3_tictactoe_terminal.py --demo
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import OUTPUTS, banner

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

ROTATION = math.pi / 4
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class TextBoard:
    def __init__(self):
        self.qc = QuantumCircuit(9, 9)            # one qubit per tile
        self.qc.h(range(9))                       # every tile starts undecided
        self.history = [[] for _ in range(9)]     # moves written on each tile

    def move(self, command):
        """Apply one text command. Returns False when the round is over."""
        parts = command.upper().split()
        if not parts:
            return True
        name, args = parts[0], [int(x) for x in parts[1:] if x.isdigit()]
        if name == "X" and args:
            self.qc.ry(-ROTATION, args[0]); self.history[args[0]].append("X")
        elif name == "O" and args:
            self.qc.ry(ROTATION, args[0]); self.history[args[0]].append("O")
        elif name == "NOT" and args:
            self.qc.x(args[0]); self.history[args[0]].append("N")
        elif name == "SWAP" and len(args) == 2 and args[0] != args[1]:
            self.qc.swap(args[0], args[1])
            self.history[args[0]].append("S"); self.history[args[1]].append("S")
        elif name == "PROB":
            self.probabilities()
        elif name == "MEASURE":
            self.measure()
            return False
        else:
            print("  Unknown command. Use: X n | O n | NOT n | SWAP a b | PROB | MEASURE")
        return True

    def show_moves(self):
        for r in range(3):
            print("  " + " | ".join(f"{3*r+c}:{''.join(self.history[3*r+c]) or '-':<5}" for c in range(3)))

    def _run(self, shots, seed=None):
        qc = self.qc.copy()
        qc.measure(range(9), range(9))
        return AerSimulator(seed_simulator=seed).run(qc, shots=shots).result().get_counts()

    def probabilities(self):
        counts = self._run(1000, seed=802)
        p_x = [sum(c for b, c in counts.items() if b[8 - i] == "0") / 1000 for i in range(9)]
        print("  Chance each tile becomes X (1000 shots):")
        for r in range(3):
            print("   " + "  ".join(f"{p_x[3*r+c]:.2f}" for c in range(3)))

    def measure(self, seed=None):
        bits = list(self._run(1, seed).keys())[0]        # one shot = one real game
        owner = ["X" if bits[8 - i] == "0" else "O" for i in range(9)]
        print("\n  Final board:")
        for r in range(3):
            print("   " + " | ".join(owner[3*r:3*r+3]))
        x = sum(all(owner[t] == "X" for t in line) for line in WIN_LINES)
        o = sum(all(owner[t] == "O" for t in line) for line in WIN_LINES)
        print(f"  X lines: {x}   O lines: {o}   ->  {'X wins' if x > o else 'O wins' if o > x else 'draw'}")
        print("\n  Game circuit:")
        print(self.qc.draw("text", fold=-1))
        (OUTPUTS / "alt_task3_last_game.txt").write_text(str(self.qc.draw("text", fold=-1)), encoding="utf-8")


if __name__ == "__main__":
    banner("Task 3 (alternative): quantum tic-tac-toe in the terminal")
    board = TextBoard()
    if "--demo" in sys.argv:
        demo = ["X 0", "X 4", "X 8", "O 2", "O 6", "PROB"]   # same moves as Game 2 in the notebook
        for cmd in demo:
            print(f"> {cmd}")
            board.move(cmd)
        board.show_moves()
        board.measure(seed=22)
    else:
        print("Commands: X n | O n | NOT n | SWAP a b | PROB | MEASURE   (tiles 0-8, row by row)")
        playing = True
        while playing:
            board.show_moves()
            playing = board.move(input("> "))
