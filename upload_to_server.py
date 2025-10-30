#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fast LAN File Upload Server with Progress Bar
Author: Tirupati Bala
Date: 26th October 2025
Description: Upload multiple files quickly over a local Wi-Fi network with real-time progress bars.

How to use:
1. Save this file as `upload_to_server.py`.
2. Install dependencies:
    pip install fastapi uvicorn python-multipart
3. Run the server:
    uvicorn upload_to_server:app --host 0.0.0.0 --port 9000
4. Access the server from any device on the same LAN:
    http://<server-ip>:9000
5. Uploaded files will be saved in the `uploads` folder and accessible at:
    http://<server-ip>:9000/uploads/<filename>
"""

import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
from pathlib import Path
from typing import List

# ---------------- Configuration ----------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload folder exists

app = FastAPI(title="LAN File Upload Server")

# Serve uploaded files for download
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ---------------- HTML Form with JS Progress Bars ----------------
UPLOAD_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>LAN File Upload with Progress</title>
</head>
<body>
    <h2>Upload multiple files to local server</h2>
    <form id="uploadForm">
        <input type="file" id="files" name="files" multiple><br><br>
        <input type="submit" value="Upload">
    </form>
    <br>
    <div id="progressContainer"></div>
    <div id="status"></div>

    <script>
        const form = document.getElementById('uploadForm');
        const progressContainer = document.getElementById('progressContainer');
        const statusDiv = document.getElementById('status');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const files = document.getElementById('files').files;
            if (files.length === 0) {
                alert("Please select at least one file.");
                return;
            }

            progressContainer.innerHTML = '';
            statusDiv.innerHTML = '';

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const progressDiv = document.createElement('div');
                progressDiv.innerHTML = `${file.name}: <progress value="0" max="100"></progress>`;
                progressContainer.appendChild(progressDiv);

                const progressBar = progressDiv.querySelector('progress');
                await uploadFile(file, progressBar);
            }

            statusDiv.innerHTML = "<b>All uploads completed!</b>";
        });

        function uploadFile(file, progressBar) {
            return new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload');

                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        const percent = (e.loaded / e.total) * 100;
                        progressBar.value = percent;
                    }
                });

                xhr.onload = () => {
                    if (xhr.status === 200) resolve();
                    else reject(xhr.statusText);
                };
                xhr.onerror = () => reject(xhr.statusText);

                const formData = new FormData();
                formData.append('files', file);
                xhr.send(formData);
            });
        }
    </script>
</body>
</html>
"""

# ---------------- Routes ----------------
@app.get("/", response_class=HTMLResponse)
def index():
    """Serve the HTML upload form"""
    return HTMLResponse(UPLOAD_FORM)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Handle multiple file uploads.
    Saves each file in the UPLOAD_DIR folder.
    """
    saved_files = []
    for file in files:
        # Sanitize filename to prevent path traversal
        safe_filename = Path(file.filename).name
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        # If file exists, append a number to avoid overwriting
        counter = 1
        original_name = Path(safe_filename).stem
        extension = Path(safe_filename).suffix
        while os.path.exists(file_path):
            safe_filename = f"{original_name}_{counter}{extension}"
            file_path = os.path.join(UPLOAD_DIR, safe_filename)
            counter += 1

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(safe_filename)

    return {"filenames": saved_files}

# ---------------- Run Server ----------------
# Command to run: uvicorn upload_to_server:app --host 0.0.0.0 --port 9000
# Access via LAN: http://<server-ip>:9000
# Uploaded files accessible at: http://<server-ip>:9000/uploads/<filename>
