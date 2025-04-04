@echo off
REM Se placer dans le dossier du script
cd /d %~dp0

REM Récupérer le chemin absolu du dossier parent (la racine du projet)
for %%I in ("..") do set "PROJECT_ROOT=%%~fI"

REM Définir les chemins nécessaires
set "SRC=%PROJECT_ROOT%\elyria\main.py"
set "RESOURCES=%PROJECT_ROOT%\resources"
set "DATA=%PROJECT_ROOT%\data"
set "DIST=%PROJECT_ROOT%\build\dist"
set "BUILD=%PROJECT_ROOT%\build\build"
set "SPEC=%PROJECT_ROOT%\build\spec"

REM Activer l’environnement virtuel
call "%PROJECT_ROOT%\venv\Scripts\activate"

REM Build avec PyInstaller
pyinstaller --onefile --windowed --name "ElyriaGame" ^
--add-data "%RESOURCES%;resources" ^
--add-data "%DATA%;data" ^
--paths "%PROJECT_ROOT%\elyria" ^
--distpath "%DIST%" ^
--workpath "%BUILD%" ^
--specpath "%SPEC%" ^
"%SRC%"

echo.
echo ✅ Build terminé ! L'exécutable est dans: %DIST%
pause
