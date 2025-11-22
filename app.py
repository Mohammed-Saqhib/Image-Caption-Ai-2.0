"""
Hugging Face Space Entry Point
AI Image Analysis Platform - Professional Edition
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set Hugging Face Space flag
os.environ['IS_HUGGINGFACE_SPACE'] = 'true'

# Import and run the app (Streamlit doesn't use if __name__ == "__main__")
try:
    from src.app_pro import *
    print("🚀 Launching AI Image Analysis Platform - Professional Edition")
    print("📍 Running on Hugging Face Space")
except ImportError as e:
    print(f"❌ Error importing app_pro: {e}")
    print("Attempting to run standard edition...")
    try:
        from src.app_enhanced import *
        print("🚀 Launching AI Image Analysis Platform - Standard Edition")
    except ImportError as e2:
        print(f"❌ Error importing app_enhanced: {e2}")
        print("Please check your installation and dependencies.")
        import streamlit as st
        st.error("Failed to load the application. Please check the logs.")
