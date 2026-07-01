#!/bin/bash
echo "Launching FastAPI Backend Services on Port 8000..."
# Notice we removed the hardcoded key line entirely. 
# It will read it directly from your terminal session's environment instead.
uvicorn app:app --host 0.0.0.0 --port 8000 &

sleep 2

echo "Launching Streamlit SOC Frontend Interface on Port 8501..."
streamlit run dashboard.py \
  --server.port 8501 \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.enableWebsocketCompression false