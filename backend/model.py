import torch
import torch.nn as nn
import ezkl
import os
import json
import asyncio
import sys

# ... (TinyModel class remains the same) ...
class TinyModel(nn.Module):
    def __init__(self):
        super(TinyModel, self).__init__()
        self.layer = nn.Linear(3, 1)
    def forward(self, x):
        return self.layer(x)

async def setup_zk_circuit():
    model = TinyModel()
    model.eval()

    # 1. Export Model & Data
    x = torch.randn(1, 3)
    input_data = {"input_data": [x.reshape([-1]).tolist()]}
    with open("input.json", "w") as f:
        json.dump(input_data, f)
    torch.onnx.export(model, x, "model.onnx", input_names=['input'], output_names=['output'])

    # 2. Generate Settings
    print("Generating settings...")
    ezkl.gen_settings("model.onnx", "settings.json")
    
    # --- NEW CODE START: Hiding the Weights ---
    print("Modifying settings for Model Privacy...")
    with open("settings.json", "r") as f:
        settings = json.load(f)

    # Set parameters (weights) to "private"
    # This removes the weights from the Verification Key (vk)
    settings["run_args"]["param_visibility"] = "private"
    
    # Ensure inputs are "public" so the User knows the model ran on THEIR data
    settings["run_args"]["input_visibility"] = "public"
    
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)
    # --- NEW CODE END ---

    print("Calibrating...")
    ezkl.calibrate_settings("input.json", "model.onnx", "settings.json", "resources")
    
    print("Compiling...")
    ezkl.compile_circuit("model.onnx", "compiled.ezkl", "settings.json")

    # 3. Setup Keys (SRS)
    srs_path = os.path.join(os.getcwd(), "kzg.srs")
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print(f"Fetching SRS to: {srs_path}")
    await ezkl.get_srs(settings_path="settings.json", srs_path=srs_path) 
    
    print("Setting up keys...")
    ezkl.setup(
        model="compiled.ezkl", 
        vk_path="vk.key", 
        pk_path="pk.key", 
        srs_path=srs_path
    )
    print("Setup complete. Weights are now HIDDEN from the Verifier.")

if __name__ == "__main__":
    asyncio.run(setup_zk_circuit())
