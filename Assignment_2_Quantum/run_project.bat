@echo off
REM ======================================================================
REM  MSE802 Assessment 2 - Quantum Project : Windows launcher
REM
REM  Double-click          -> sets up Python (first time) and shows a menu
REM  run_project.bat all   -> runs Tasks 1, 2, 3 and 4 together
REM  run_project.bat 2     -> runs only Task 2 (also 1, 3, 4)
REM  run_project.bat alt   -> runs the alternative code
REM
REM  Outputs: inside each notebook, in each task's results\ folder,
REM           and as web pages in outputs_html\  (open with any browser)
REM ======================================================================
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.12 or newer from python.org and tick "Add to PATH".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo First run: creating the virtual environment .venv ...
    python -m venv .venv
)
call ".venv\Scripts\activate.bat"

if not exist ".venv\installed.flag" (
    echo Installing packages from requirements.txt - this takes a few minutes the first time ...
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo Package installation failed. See MAINTENANCE.md - Common problems.
        pause
        exit /b 1
    )
    python -m ipykernel install --user --name python3 --display-name "Python 3 (MSE802)" >nul 2>nul
    echo ok> ".venv\installed.flag"
)

python run_project.py %*

echo.
echo Done. Open the outputs_html folder to see the results in your browser.
pause
