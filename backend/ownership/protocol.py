import json
import numpy as np
from .corrupt import corrupt_model
from .restore import restore_model
from .weight_index import WeightIndex
from .derive_indices import derive_indices

def respond_to_challenge(model_path, secret_key, challenge_hex, k=200):
    challenge = bytes.fromhex(challenge_hex)

    # corrupt
    corrupted = corrupt_model(model_path, secret_key, challenge, k)

    # compute inference difference (example placeholder)
    l2_diff = float(np.random.rand() / 100)  # replace with your real inference test

    # restore
    restore_model(model_path, secret_key, challenge, k, verbose = True)

    report = {
        "challenge": challenge_hex,
        "k": k,
        "epsilon": 1e-3,
        "l2_difference": l2_diff,
        "corrupted_preview": corrupted[:5]
    }

    return report
