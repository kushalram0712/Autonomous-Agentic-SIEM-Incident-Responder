import threading
import uvicorn
import os
import subprocess

def run_backend():
    # Bind to localhost inside the container environment
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Grab the dynamic port assigned by Hugging Face (defaults to 7860)
    port = os.environ.get("PORT", "7860")
    
    subprocess.run([
        "streamlit", "run", "dashboard.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.enableWebsocketCompression", "false"
    ])