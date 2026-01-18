# Running the Model Ownership Protocol (Local Two-Window Demo)

This project demonstrates neural network ownership verification using deterministic weight corruption and restoration on ONNX models.

The demo runs locally using two terminals:

* **Verifier window** – generates a challenge
* **Prover window** – corrupts + restores the model and responds

No server is required.

---

## 1. Prerequisites

* Python **3.9+**
* Git
* Linux / macOS / Windows (WSL works)

---

## 2. Clone the repository

```bash
git clone https://github.com/shreesha84/zero-knowledge-proof.git
cd zero-knowledge-proof
```

---

## 3. Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate        # Linux / macOS
# OR
env\Scripts\activate           # Windows
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Move to backend directory

```bash
cd backend
```

---

## 6. Terminal 1 – Start the verifier

Open a new terminal, activate the same environment, then:

```bash
cd zero-knowledge-proof/backend
python verifier_app.py
```

You will see:

```
Challenge generated: <hex string>
Waiting for prover...
```

This creates `challenge.json`.

---

## 7. Terminal 2 – Start the prover

In another terminal:

```bash
cd zero-knowledge-proof/backend
source ../env/bin/activate     # if not already active
python prover_app.py
```

You will see:

* the received challenge
* corrupted weight preview
* output difference
* model restoration confirmation

This creates `report.json`.

---

## 8. Verifier completes automatically

Return to Terminal 1.

You should see:

```
=== REPORT RECEIVED ===
Corruption confirmed
Ownership protocol completed.
```

---

## 9. What just happened

1. Verifier generated a random challenge
2. Prover deterministically corrupted hidden model weights
3. Model output changed
4. Prover restored the model
5. Verifier confirmed the response

This proves ownership without revealing model weights.

---

## 10. Notes

* The demo uses a small ONNX model (`model_small.onnx`) included in the repo.
* No trained private models or keys are required.
* Temporary files created during execution:

  * `challenge.json`
  * `report.json`

These can be deleted after each run.

---

## 11. Troubleshooting

If you see missing package errors:

```bash
pip install -r requirements.txt
```

If ONNX fails to load:

```bash
pip install onnx onnxruntime numpy
```

---

.
