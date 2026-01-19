import json
import numpy as np
import onnxruntime as ort

from ownership.corrupt import corrupt_model
from ownership.restore import restore_model


def run_inference(model_path: str) -> np.ndarray:
    """
    Run inference on the ONNX model using an automatically
    generated deterministic input matching the model shape.
    """

    sess = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])

    input_meta = sess.get_inputs()[0]
    input_name = input_meta.name
    input_shape = input_meta.shape

    # Handle dynamic shapes safely
    batch_dim = 1
    feature_dim = input_shape[1]

    if isinstance(feature_dim, str) or feature_dim is None:
        raise ValueError("Model input dimension must be fixed for this demo.")

    input_data = np.ones((batch_dim, feature_dim), dtype=np.float32)

    outputs = sess.run(None, {input_name: input_data})

    return outputs[0]


def respond_to_challenge(
    model_path: str,
    secret_key: bytes,
    challenge_hex: str,
    k: int = 200,
):
    """
    Execute the ownership protocol:
    1. Run inference on clean model
    2. Corrupt secret weights
    3. Run inference again
    4. Compute L2 difference
    5. Restore model
    6. Return report
    """

    challenge = bytes.fromhex(challenge_hex)

    # Inference before corruption
    y_clean = run_inference(model_path)

    # Corrupt model
    corrupted_indices = corrupt_model(
        model_path, secret_key, challenge, k, verbose=False
    )

    # Inference after corruption
    y_corrupt = run_inference(model_path)

    # L2 difference
    l2_difference = float(np.linalg.norm(y_clean - y_corrupt))

    # Restore model
    restore_model(model_path, secret_key, challenge, k, verbose=False)

    report = {
        "challenge": challenge_hex,
        "k": k,
        "epsilon": 1e-3,
        "l2_difference": l2_difference,
        "corrupted_preview": corrupted_indices[:5],
    }

    return report
