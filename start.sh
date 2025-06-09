#!/bin/bash

uvicorn app.main:app --host 0.0.0.0 --port 8501 &

streamlit run app/streamlit_app.py --server.port 8080 --server.address=0.0.0.0