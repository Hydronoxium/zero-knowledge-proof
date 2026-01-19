import { useState } from "react";

export default function UploadModel() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a .onnx file");
      return;
    }

    const formData = new FormData();
    formData.append("model", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setStatus(`Uploaded: ${data.filename}`);
    } catch (err) {
      setStatus("Upload failed");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload ONNX Model</h2>

      <input
        type="file"
        accept=".onnx"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <br /><br />

      <button onClick={handleUpload}>Upload</button>

      <p>{status}</p>
    </div>
  );
}
