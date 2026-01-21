import subprocess
import os

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_cmd(cmd: list[str]):
    print("\n[ezkl] Running:", " ".join(cmd))
    print("[ezkl] CWD:", BACKEND_DIR)

    result = subprocess.run(
        cmd,
        cwd=BACKEND_DIR,
        capture_output=True,
        text=True
    )

    print("[ezkl] STDOUT:\n", result.stdout)
    print("[ezkl] STDERR:\n", result.stderr)
    print("[ezkl] Return code:", result.returncode)

    if result.returncode != 0:
        raise RuntimeError("Command failed")

    return result.stdout



def generate_ezkl_proof(compiled_circuit_path: str, input_json: str = "input.json"):

    print("[ezkl] backend dir:", BACKEND_DIR)

    run_cmd([
        "ezkl", "gen-witness",
        "--compiled-circuit", compiled_circuit_path,
        "--data", input_json
    ])

    run_cmd([
        "ezkl", "prove",
        "--compiled-circuit", compiled_circuit_path
    ])

    proof_path = os.path.join(BACKEND_DIR, "proof.json")
    

    

    if not os.path.exists(proof_path):
        raise RuntimeError("proof.json was not generated")

    print("[ezkl] Proof generated at:", proof_path)

    return proof_path


def verify_ezkl_proof(proof_path: str, vk_path: str):

    result = subprocess.run(
        ["ezkl", "verify", "--proof-path", proof_path, "--vk-path", vk_path],
        cwd=BACKEND_DIR,
        capture_output=True,
        text=True
    )

    return result.returncode == 0
