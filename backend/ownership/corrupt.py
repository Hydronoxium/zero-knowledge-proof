"""
Load the ONNX model (including external data)

Enumerate weights (using WeightIndex)

Derive the k special indices (using derive_indices)

Modify those weights slightly

Save the corrupted model safely
"""
import os
import onnx
from onnx import numpy_helper
import numpy as np

from ownership.weight_index import WeightIndex
from ownership.derive_indices import derive_indices


EPSILON = 1e-3


def corrupt_model(model_path: str, secret_key: bytes, challenge: bytes, k: int = 20, verbose=False):
    """
    Corrupt k secret weights in the ONNX model deterministically using secret_key and challenge.
    """

    # Load model with external data
    model = onnx.load(model_path, load_external_data=True)

    # Build weight index
    wi = WeightIndex(model_path)
    total_weights = wi.build()

    # Derive global indices
    indices = derive_indices(secret_key, challenge, k, total_weights)

    # Map tensor name -> numpy array (copy)
    tensor_map = {}
    for tensor in model.graph.initializer:
        tensor_map[tensor.name] = numpy_helper.to_array(tensor)

    corrupted_info = []

    # Apply corruption
    for global_idx in indices:
        tensor_name, local_idx = wi.resolve(global_idx)
        arr = tensor_map[tensor_name]

        flat = arr.flatten()

        old_val = float(flat[local_idx])
        flat[local_idx] += EPSILON
        new_val = float(flat[local_idx])

        tensor_map[tensor_name] = flat.reshape(arr.shape)

        if verbose:
            corrupted_info.append(
                (tensor_name, int(local_idx), old_val, new_val)
            )

    # Write back modified tensors
    for tensor in model.graph.initializer:
        new_arr = tensor_map[tensor.name]
        new_tensor = numpy_helper.from_array(new_arr, tensor.name)

        tensor.ClearField("raw_data")
        tensor.CopyFrom(new_tensor)

    # Remove existing external data file if present
    data_path = model_path + ".data"
    if os.path.exists(data_path):
        os.remove(data_path)

    onnx.save_model(
        model,
        model_path,
        save_as_external_data=True,
        all_tensors_to_one_file=True,
        location=os.path.basename(data_path)
    )



    if verbose:
        return corrupted_info
    else:
        return indices

