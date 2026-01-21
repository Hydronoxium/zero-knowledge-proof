import json, os, secrets, time
from ownership.ezkl_utils import verify_ezkl_proof

SESSION_TIMEOUT = 300  # seconds

def now():
    return int(time.time())

for f in ["challenge.json", "report.json"]:
    if os.path.exists(f):
        os.remove(f)

session_id = secrets.token_hex(16)
challenge = secrets.token_hex(16)
timestamp = now()

challenge_obj = {
    "session_id": session_id,
    "challenge": challenge,
    "timestamp": timestamp,
}

with open("challenge.json", "w") as f:
    json.dump(challenge_obj, f)

print("Session ID:", session_id)
print("Challenge:", challenge)
print("Waiting for prover...")

while not os.path.exists("report.json"):
    time.sleep(1)

with open("report.json") as f:
    report = json.load(f)

# ---- Validation ----

if report.get("session_id") != session_id:
    print("❌ Session ID mismatch")
    exit(1)

if report.get("challenge") != challenge:
    print("❌ Challenge mismatch")
    exit(1)

if now() - report.get("timestamp", 0) > SESSION_TIMEOUT:
    print("❌ Session expired")
    exit(1)

proof_path = report["proof_path"]

if not verify_ezkl_proof(proof_path, "vk_reference.key"):
    print("❌ ZK proof invalid")
    exit(1)

print("\n✅ ZK proof valid")
print("✅ Challenge verified")
print("✅ Session valid")

if report["l2_difference"] > 0:
    print("✅ Corruption confirmed")

print("\n=== REPORT ===")
print(json.dumps(report, indent=2))

print("\nOwnership protocol completed successfully.")
