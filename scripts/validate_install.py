import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")

required_files = [
    "model.onnx",
    "compiled_reference.ezkl",
    "pk_reference.key",
    "vk_reference.key",
    "input.json",
]

def fail(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def ok(msg):
    print(f"✅ {msg}")

print("\n--- Validating installation ---\n")

# Python packages
try:
    import onnx
    import onnxruntime
    import numpy
except Exception as e:
    fail(f"Python dependencies missing: {e}")

ok("Python dependencies installed")

# ezkl binary
if not shutil.which("ezkl"):
    fail("ezkl binary not found in PATH")

ok("ezkl binary found")

# Required files
for f in required_files:
    path = os.path.join(BACKEND, f)
    if not os.path.exists(path):
        fail(f"Missing required file: {f}")
    ok(f"Found {f}")

# Reference keys (explicit)
if not os.path.exists(os.path.join(BACKEND, "pk_reference.key")):
    fail("Missing pk_reference.key")
ok("Found pk_reference.key")

if not os.path.exists(os.path.join(BACKEND, "vk_reference.key")):
    fail("Missing vk_reference.key")
ok("Found vk_reference.key")

# Working key copies (optional – auto-created)
if not os.path.exists(os.path.join(BACKEND, "pk.key")):
    ok("pk.key will be created automatically when needed")

if not os.path.exists(os.path.join(BACKEND, "vk.key")):
    ok("vk.key will be created automatically when needed")

# SRS
srs_path = os.path.expanduser("~/.ezkl/srs/kzg17.srs")
if not os.path.exists(srs_path):
    fail("Missing SRS file ~/.ezkl/srs/kzg17.srs")

ok("SRS file exists")

# Quick ezkl sanity test
print("\nRunning ezkl verify dry check...")

try:
    subprocess.run(
        ["ezkl", "--version"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
except Exception:
    fail("ezkl execution failed")

ok("ezkl runs correctly")

print("\nInstallation validated successfully.")
