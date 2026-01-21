import torch
import torch.nn as nn


class BigModel(nn.Module):
    def __init__(self, input_dim=128, hidden_dim=512, layers=4, output_dim=10):
        super().__init__()

        modules = []
        dim = input_dim

        for _ in range(layers):
            modules.append(nn.Linear(dim, hidden_dim))
            modules.append(nn.ReLU())
            dim = hidden_dim

        modules.append(nn.Linear(dim, output_dim))

        self.net = nn.Sequential(*modules)

    def forward(self, x):
        return self.net(x)


def main():
    model = BigModel(
        input_dim=128,
        hidden_dim=512,
        layers=4,
        output_dim=10
    )

    model.eval()

    dummy_input = torch.randn(1, 128)

    output_path = "big_model.onnx"

    import onnx

# Export normally first
    torch.onnx.export(
        model,
        dummy_input,
        "big_model_raw.onnx",
        input_names=["input"],
        output_names=["output"],
        opset_version=13,
        do_constant_folding=True
    )

    # Reload and re-save as single-file ONNX
    model_onnx = onnx.load("big_model_raw.onnx")

    onnx.save_model(
        model_onnx,
        "big_model.onnx",
        save_as_external_data=False
    )

    print("Saved single-file ONNX model: big_model.onnx")




    total_params = sum(p.numel() for p in model.parameters())

    print("Model exported to:", output_path)
    print("Total parameters:", total_params)


if __name__ == "__main__":
    main()
