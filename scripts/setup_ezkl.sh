#!/usr/bin/env bash
set -e

echo "======================================"
echo " EZKL Ownership Protocol Setup Script "
echo "======================================"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

cd "$BACKEND_DIR"

echo "[1/8] Checking Python environment..."
python -c "import sys; print(sys.version)"

echo "[2/8] Checking ezkl installation..."
if ! command -v ezkl &> /dev/null; then
    echo "❌ ezkl not found. Install with: pip install ezkl"
    exit 1
fi

echo "[3/8] Cleaning previous artifacts..."
rm -f big_model.onnx big_model.onnx.data model.onnx model.onnx.data
rm -f compiled_reference.ezkl
rm -f pk_reference.key vk_reference.key
rm -f witness.json proof.json challenge.json report.json

echo "[4/8] Generating large ONNX model..."
python create_big_model.py

# Rename generated model to expected name
if [ -f big_model.onnx ]; then
    mv big_model.onnx model.onnx
fi

if [ ! -f model.onnx ]; then
    echo "❌ model.onnx was not generated"
    exit 1
fi


echo "[5/8] Compiling model with ezkl..."
ezkl compile-circuit -M model.onnx

if [ ! -f model.compiled ]; then
    echo "❌ model.compiled not generated"
    exit 1
fi

mv model.compiled compiled_reference.ezkl

echo "[6/8] Generating SRS (if missing)..."
SRS_PATH="$HOME/.ezkl/srs/kzg17.srs"

if [ ! -f "$SRS_PATH" ]; then
    mkdir -p "$HOME/.ezkl/srs"
    ezkl gen-srs --srs-path "$SRS_PATH" --logrows 17
fi

echo "[7/8] Running ezkl setup..."
ezkl setup --compiled-circuit compiled_reference.ezkl

if [ ! -f pk.key ] || [ ! -f vk.key ]; then
    echo "❌ Setup failed: pk.key or vk.key missing"
    exit 1
fi

mv pk.key pk_reference.key
mv vk.key vk_reference.key

# Create working copies for ezkl CLI
cp pk_reference.key pk.key
cp vk_reference.key vk.key


echo "[8/8] Final validation..."

python ../scripts/validate_install.py

echo "======================================"
echo " Setup completed successfully ✅"
echo "======================================"
