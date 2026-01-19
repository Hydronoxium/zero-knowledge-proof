import json, os, secrets, time
import os

if os.path.exists("challenge.json"):
    os.remove("challenge.json")

if os.path.exists("report.json"):
    os.remove("report.json")

challenge = secrets.token_hex(16)

with open("challenge.json", "w") as f:
    json.dump({"challenge": challenge}, f)

print("Challenge generated:", challenge)
print("Waiting for prover...")

while not os.path.exists("report.json"):
    time.sleep(1)

with open("report.json") as f:
    report = json.load(f)

print("\n=== REPORT RECEIVED ===")
print(json.dumps(report, indent=2))

if report["challenge"] != challenge:
    print("❌ Challenge mismatch")
elif report["l2_difference"] > 0:
    print("✅ Corruption confirmed")
else:
    print("❌ No observable corruption")

print("\nOwnership protocol completed.")
