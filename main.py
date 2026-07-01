import threading
import uvicorn
import os
import subprocess

# 1. Background thread worker to run the FastAPI event loop
def run_backend():
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    # Start the backend pipeline thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # 2. Start the primary Streamlit application instance on the port assigned by the host environment
    port = os.environ.get("PORT", "8501")
    subprocess.run([
        "streamlit", "run", "dashboard.py",
        "--server.port", port,
        "--server.address", "0.0.0.5",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ])