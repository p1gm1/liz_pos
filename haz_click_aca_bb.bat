@echo off
echo "Creating venv..."
python -m venv .venv
call .venv\Scripts\activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Building executable..."
python -m streamlit run src/main.py
echo "Build finished."
pause
