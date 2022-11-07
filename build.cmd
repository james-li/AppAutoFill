@echo off
rmdir /s /q dist
pyinstaller --windowed -i ../guanjiaNativeTools/img/app.ico -y --clean --win-private-assemblies --onefile AppLauncher.py
move /Y dist\*.exe .
