import torch
import torch.nn as nn
import ezkl
import os
import json
import asyncio
import sys

class TinyModel(nn.Module):
    def __init__(self):
        super(TinyModel, self).__init__()
        self.layer = nn.Linear(3, 1)
    # creates a sample small model, after frontend is done we will take input from user
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

    # 2. Basic Setup
    print("Generating settings...")
    ezkl.gen_settings("model.onnx", "settings.json")
    
    print("Calibrating...")
    ezkl.calibrate_settings("input.json", "model.onnx", "settings.json", "resources")
    
    print("Compiling...")
    ezkl.compile_circuit("model.onnx", "compiled.ezkl", "settings.json")

    # 3. THE FIX: Explicit SRS Path
    # We define exactly where the SRS file should be saved/read from.
    srs_path = os.path.join(os.getcwd(), "kzg.srs")
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print(f"Fetching SRS to: {srs_path}")
    # We pass srs_path explicitly to override the 'NotPresent' default
    await ezkl.get_srs(settings_path="settings.json", srs_path=srs_path) 
    
    print("Setting up keys...")
    # We must pass the same srs_path here so setup knows where to find it
    ezkl.setup(
        model="compiled.ezkl", 
        vk_path="vk.key", 
        pk_path="pk.key", 
        srs_path=srs_path
    )

    print("Setup complete.")

if __name__ == "__main__":
    asyncio.run(setup_zk_circuit())