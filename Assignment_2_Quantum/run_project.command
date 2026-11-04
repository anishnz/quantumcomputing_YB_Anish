#!/usr/bin/env bash
# ======================================================================
#  MSE802 Assessment 2 - Quantum Project : macOS launcher (double-click)
#
#  Double-click in Finder  -> Terminal opens, sets up Python the first
#                             time, then shows the menu (1-4, A, L, S, C)
#  If macOS says it cannot be opened: right-click -> Open -> Open,
#  or in Terminal run:  chmod +x run_project.command
#  Needs Python 3.12+ (python.org installer or: brew install python)
# ======================================================================
cd "$(dirname "$0")"                                   # work inside the project folder
if ! command -v python3 >/dev/null 2>&1; then          # Python must be installed
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/macos/"
  read -r -p "Press Enter to close..." _; exit 1
fi
if [ ! -f ".venv/installed.flag" ]; then               # first run only
  echo "First run: creating .venv and installing packages (a few minutes) ..."
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade pip -q
  .venv/bin/python -m pip install -r requirements.txt -q || { echo "Install failed - see MAINTENANCE.md"; read -r _; exit 1; }
  .venv/bin/python -m ipykernel install --user --name python3 --display-name "Python 3 (MSE802)" >/dev/null 2>&1
  echo ok > .venv/installed.flag
fi
.venv/bin/python run_project.py "$@"                   # menu, or the argument given
echo "Done. Open the outputs_html folder to see every result in a browser."
read -r -p "Press Enter to close this window..." _
