@echo off
echo "Creating venv..."
python -m venv .venv
call .venv\Scripts\activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Building executable..."
start "" pythonw.exe -m streamlit run src/main.py
echo "Build finished."
pause
