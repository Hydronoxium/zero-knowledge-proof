from ownership.ezkl_utils import verify_ezkl_proof
import json, os, secrets, time

# Clean stale files
if os.path.exists("challenge.json"):
    os.remove("challenge.json")

if os.path.exists("report.json"):
    os.remove("report.json")

# Generate challenge
challenge = secrets.token_hex(16)

with open("challenge.json", "w") as f:
    json.dump({"challenge": challenge}, f)

print("Challenge generated:", challenge)
print("Waiting for prover...")

# Wait for prover response
while not os.path.exists("report.json"):
    time.sleep(1)

with open("report.json") as f:
    report = json.load(f)

# ---- ZK verification ----

proof_path = report.get("proof_path")

if not proof_path or not os.path.exists(proof_path):
    print("❌ Missing proof file.")
    exit(1)

ok = verify_ezkl_proof(proof_path, "vk_reference.key")

if not ok:
    print("❌ ZK proof verification FAILED.")
    exit(1)

print("✅ ZK proof verification succeeded.")
print("Ownership verified.")

# ---- Protocol checks ----

print("\n=== REPORT RECEIVED ===")
print(json.dumps(report, indent=2))

if report.get("challenge") != challenge:
    print("❌ Challenge mismatch")
elif report.get("l2_difference", 0) > 0:
    print("✅ Corruption confirmed")
else:
    print("❌ No observable corruption")

print("\nOwnership protocol completed.")
