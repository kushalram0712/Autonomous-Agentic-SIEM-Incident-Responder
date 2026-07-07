#!/bin/bash
echo "Launching FastAPI Backend Services on Port 8000..."

uvicorn app:app --host 0.0.0.0 --port 8000 &

sleep 2

echo "Launching Streamlit SOC Frontend Interface on Port 8501..."
streamlit run dashboard.py \
  --server.port 8501 \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.enableWebsocketCompression false
