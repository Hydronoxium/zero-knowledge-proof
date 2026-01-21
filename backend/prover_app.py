import json
import os
import time

from ownership.protocol import respond_to_challenge

MODEL_PATH = "model.onnx"
SECRET_KEY = b"demo_secret_key_123"  # replace for production


def wait_for_challenge():
    print("Waiting for challenge...")

    while not os.path.exists("challenge.json"):
        time.sleep(1)

    with open("challenge.json") as f:
        challenge_obj = json.load(f)

    return challenge_obj


def main():
    challenge_obj = wait_for_challenge()

    session_id = challenge_obj["session_id"]
    challenge = challenge_obj["challenge"]
    timestamp = challenge_obj["timestamp"]

    print("Received challenge:", challenge)
    print("Session ID:", session_id)

    report = respond_to_challenge(
        MODEL_PATH,
        SECRET_KEY,
        challenge,
    )

    report["session_id"] = session_id
    report["timestamp"] = timestamp

    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n=== CORRUPTION REPORT ===")
    print(json.dumps(report, indent=2))

    print("\nModel restored.")
    print("Report written to report.json")


if __name__ == "__main__":
    main()
