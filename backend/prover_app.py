import json
from ownership.protocol import respond_to_challenge

SECRET_KEY = b"test_secret_123"
MODEL_PATH = "big_model.onnx"

with open("challenge.json") as f:
    challenge_hex = json.load(f)["challenge"]

print("Received challenge:", challenge_hex)

report = respond_to_challenge(MODEL_PATH, SECRET_KEY, challenge_hex)

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

print("\n=== CORRUPTION REPORT ===")
print(json.dumps(report, indent=2))
print("\nModel restored.")
