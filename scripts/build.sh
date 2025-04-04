#!/bin/bash

cd "$(dirname "$0")"

PROJECT_ROOT="$(realpath ..)"
SRC="$PROJECT_ROOT/elyria/main.py"
RESOURCES="$PROJECT_ROOT/resources"
DATA="$PROJECT_ROOT/data"
DIST="$PROJECT_ROOT/build/dist"
BUILD="$PROJECT_ROOT/build/build"
SPEC="$PROJECT_ROOT/build/spec"

source "$PROJECT_ROOT/venv/bin/activate"

pyinstaller --onefile --windowed --name "Elyria" \
--add-data "$RESOURCES:resources" \
--add-data "$DATA:data" \
--paths "$PROJECT_ROOT/elyria" \
--distpath "$DIST" \
--workpath "$BUILD" \
--specpath "$SPEC" \
"$SRC"

echo ""
echo "✅ Build terminé ! L'exécutable est dans $DIST/"
