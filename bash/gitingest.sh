#!/usr/bin/env bash

# Ukončit skript při jakékoliv chybě
set -e

# 1. Kontrola, zda je gitingest nainstalován
if ! command -v gitingest &> /dev/null; then
    echo "❌ Příkaz 'gitingest' nebyl nalezen. Nainstalujte ho pomocí: pip install gitingest"
    exit 1
fi

# 2. Vytvoření cílové složky, pokud neexistuje
OUTPUT_DIR="output/gitingest"
mkdir -p "$OUTPUT_DIR"

echo "⏳ Generuji gitingest soubory v '$OUTPUT_DIR'..."

# 3. Spuštění gitingest pro source.txt
gitingest . \
  --output "$OUTPUT_DIR/sorce.txt" \
  --exclude-pattern "*.svg,*.excalidraw"

# 4. Spuštění gitingest pro pages.txt
gitingest . \
  --output "$OUTPUT_DIR/pages.txt" \
  --exclude-pattern "*.svg"

echo "✅ Hotovo! Soubory byly uloženy do:"
echo "   - $OUTPUT_DIR/sorce.txt"
echo "   - $OUTPUT_DIR/pages.txt"
