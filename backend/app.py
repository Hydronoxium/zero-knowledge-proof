from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploaded_models"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_model(model: UploadFile = File(...)):
    if not model.filename.endswith(".onnx"):
        return {"error": "Only .onnx allowed"}

    path = os.path.join(UPLOAD_DIR, model.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(model.file, f)

    return {"filename": model.filename}
