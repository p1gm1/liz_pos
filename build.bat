@echo off
REM Check for Python
where python >nul 2>nul
if %errorlevel% == 0 (
    echo Python is already installed.
    goto :build
)

echo Python is not installed.
echo Attempting to install Python using Chocolatey...

REM Check for Chocolatey
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo Chocolatey is not installed. Please install Chocolatey first, or install Python manually.
    echo For more information on installing Chocolatey, visit https://chocolatey.org/install
    pause
    exit /b 1
)

REM Install Python using Chocolatey
choco install python -y
if %errorlevel% neq 0 (
    echo Failed to install Python using Chocolatey. Please install Python manually.
    pause
    exit /b 1
)

echo Python installed successfully. Please re-run the build script.
pause
exit /b 0

:build
echo "Creating venv..."
python -m venv .venv
call .venv\Scripts\activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Building executable..."
pyinstaller --name "liz-pos" --onefile --windowed --add-data "src;src" src/main.py
echo "Build finished."
pause