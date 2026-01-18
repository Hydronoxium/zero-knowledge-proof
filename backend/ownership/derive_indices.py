import hmac
import hashlib
import struct

def derive_indices(secret_key: bytes, challenge: bytes, k: int, total_weights: int):
    if k > total_weights:
        raise ValueError(
            f"Cannot select {k} unique indices from only {total_weights} weights"
        )

    indices = []
    used = set()
    counter = 0

    while len(indices) < k:
        msg = challenge + struct.pack(">I", counter)
        digest = hmac.new(secret_key, msg, hashlib.sha256).digest()

        value = int.from_bytes(digest[:8], "big")
        idx = value % total_weights

        if idx not in used:
            used.add(idx)
            indices.append(idx)

        counter += 1

    return indices

