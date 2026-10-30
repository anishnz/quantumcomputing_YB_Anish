"""Shared set-up for the alternative scripts: find the project's common helper and the output folder."""
import sys
from pathlib import Path

ALT_DIR = Path(__file__).resolve().parent            # .../Assignment_2_Quantum/Alternative_Code
PROJECT_DIR = ALT_DIR.parent                         # .../Assignment_2_Quantum
OUTPUTS = ALT_DIR / "outputs"                        # every alternative script saves its files here
OUTPUTS.mkdir(exist_ok=True)

sys.path.insert(0, str(PROJECT_DIR / "common"))      # so "import quokka_helper" works from any folder
import quokka_helper as qh                           # noqa: E402  (same helper as the main notebooks)

SHOTS = 1000                                         # same shot count as the main tasks


def banner(title):
    """Print a clear heading in the terminal."""
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)
