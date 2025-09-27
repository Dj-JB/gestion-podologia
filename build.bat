@echo off
echo Building gestion_podologia.exe locally...
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed gestion_podologia.py
echo Done. Check the dist\ folder for gestion_podologia.exe
pause
