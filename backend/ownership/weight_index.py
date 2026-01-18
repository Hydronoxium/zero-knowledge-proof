import onnx
import math


class WeightIndex:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.ranges = []   # (tensor_name, start, end)
        self.total_weights = 0

    def build(self):
        model = onnx.load(self.model_path, load_external_data=False)

        offset = 0
        for tensor in model.graph.initializer:
            size = 1
            for d in tensor.dims:
                size *= d

            self.ranges.append((tensor.name, offset, offset + size))
            offset += size

        self.total_weights = offset
        return self.total_weights

    def resolve(self, global_index: int):
        for name, start, end in self.ranges:
            if start <= global_index < end:
                return name, global_index - start

        raise IndexError("Global index out of range")
