@echo off
echo "Creating venv..."
python -m venv .venv
call .venv\Scripts\activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Building executable..."
pyinstaller --name "liz-pos" --onefile --windowed --add-data "src;src" src/main.py
echo "Build finished."
pause
