import os
import numpy as np
import onnxruntime as ort

from ownership.corrupt import corrupt_model
from ownership.restore import restore_model


def run_inference(model_path: str) -> np.ndarray:
    """
    Run inference on the ONNX model using a deterministic input
    generated from the model's input shape.
    """

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    sess = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"]
    )

    input_meta = sess.get_inputs()[0]
    input_name = input_meta.name
    input_shape = input_meta.shape

    # Expect shape [batch, features]
    batch_size = 1
    feature_dim = input_shape[1]

    if feature_dim is None or isinstance(feature_dim, str):
        raise ValueError(
            "Model input dimension must be fixed (no dynamic dims) for this demo."
        )

    # Deterministic input (important for reproducibility)
    input_data = np.ones(
        (batch_size, feature_dim),
        dtype=np.float32
    )

    outputs = sess.run(None, {input_name: input_data})

    return outputs[0]


def respond_to_challenge(
    model_path: str,
    secret_key: bytes,
    challenge_hex: str,
    k: int = 200,
) -> dict:
    """
    Ownership protocol executed by the PROVER.

    Parameters
    ----------
    model_path : str
        Path to uploaded .onnx model
    secret_key : bytes
        Owner secret
    challenge_hex : str
        Verifier challenge (hex encoded)
    k : int
        Number of corrupted weights

    Returns
    -------
    dict
        Proof report to send to verifier
    """

    if not model_path.endswith(".onnx"):
        raise ValueError("Uploaded file must be a .onnx model")

    challenge = bytes.fromhex(challenge_hex)

    # 1️⃣ Inference on clean model
    y_clean = run_inference(model_path)

    # 2️⃣ Corrupt secret weights
    corrupted_indices = corrupt_model(
        model_path,
        secret_key,
        challenge,
        k=k,
        verbose=False
    )

    # 3️⃣ Inference after corruption
    y_corrupt = run_inference(model_path)

    # 4️⃣ Measure functional change
    l2_difference = float(np.linalg.norm(y_clean - y_corrupt))

    # 5️⃣ Restore model
    restore_model(
        model_path,
        secret_key,
        challenge,
        k=k,
        verbose=False
    )

    # 6️⃣ Prepare report
    report = {
        "model": os.path.basename(model_path),
        "challenge": challenge_hex,
        "k": k,
        "epsilon": 1e-3,
        "l2_difference": l2_difference,
        "corrupted_preview": corrupted_indices[:5],
    }

    return report
