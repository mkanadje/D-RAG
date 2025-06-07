#!/bin/bash

uvicorn app.main:app --host 0.0.0.0 --port 8080 &

streamlit run ui/ui.py --server.port 8501 --server.address=0.0.0.0