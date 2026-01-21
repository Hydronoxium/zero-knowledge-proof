import json
import time

from ownership.protocol import respond_to_challenge

MODEL_PATH = "big_model.onnx"
SECRET_KEY = b"super_secret_owner_key"

# Wait for challenge
while True:
    try:
        with open("challenge.json") as f:
            challenge_hex = json.load(f)["challenge"]
        break
    except FileNotFoundError:
        time.sleep(1)

print("Received challenge:", challenge_hex)

report = respond_to_challenge(
    MODEL_PATH,
    SECRET_KEY,
    challenge_hex,
    k=200
)

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Report written.")
print("Proof path:", report["proof_path"])
