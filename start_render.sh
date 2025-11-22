#!/bin/bash

# Render.com start script for AI Image Analysis Pro
streamlit run src/app_pro.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true
