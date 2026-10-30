#!/usr/bin/env bash
# MSE802 Assessment 2 - launcher for macOS / Linux
#   ./run_project.sh          -> menu
#   ./run_project.sh all      -> Tasks 1-4 together
#   ./run_project.sh 3        -> only Task 3
set -e
cd "$(dirname "$0")"
if [ ! -x ".venv/bin/python" ]; then
  echo "First run: creating .venv and installing packages ..."
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade pip -q
  .venv/bin/python -m pip install -r requirements.txt -q
  .venv/bin/python -m ipykernel install --user --name python3 >/dev/null 2>&1 || true
fi
.venv/bin/python run_project.py "$@"
echo "Done. Open outputs_html/ in a browser to see the results."
