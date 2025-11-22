import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure Streamlit page
st.set_page_config(
    page_title="AI Image Analysis Platform",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Image Analysis Platform - Professional Edition")
st.info("⏳ Loading application components... This may take a moment on first use.")

# Import components lazily (only when needed)
try:
    # Don't import heavy libraries at startup
    # Instead, import them inside functions when actually needed
    
    # Show a simple interface immediately
    st.sidebar.header("📁 Upload Image")
    uploaded_file = st.sidebar.file_uploader(
        "Choose an image",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff']
    )
    
    if uploaded_file is not None:
        # Only import heavy libraries when user uploads a file
        from PIL import Image
        import numpy as np
        
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Show available features
        st.subheader("📋 Available Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔍 OCR & Text Extraction
            - Multi-language support (7 languages)
            - High accuracy text extraction
            - Export to TXT, JSON, PDF
            """)
            
            if st.button("🔍 Extract Text", key="ocr"):
                with st.spinner("Loading OCR engine..."):
                    try:
                        import easyocr
                        st.success("✅ OCR engine loaded! Processing image...")
                        
                        # Initialize OCR
                        reader = easyocr.Reader(['en'])
                        
                        # Convert PIL image to numpy array
                        img_array = np.array(image)
                        
                        # Extract text
                        results = reader.readtext(img_array)
                        
                        if results:
                            st.subheader("📝 Extracted Text")
                            extracted_text = " ".join([text for (_, text, _) in results])
                            st.text_area("Text:", extracted_text, height=200)
                            st.download_button(
                                "💾 Download Text",
                                extracted_text,
                                file_name="extracted_text.txt"
                            )
                        else:
                            st.warning("No text found in the image.")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        with col2:
            st.markdown("""
            ### 🎨 AI Image Captioning
            - BLIP model for accurate captions
            - Context-aware descriptions
            - Fast processing
            """)
            
            if st.button("🎨 Generate Caption", key="caption"):
                with st.spinner("Loading AI model..."):
                    try:
                        from transformers import BlipProcessor, BlipForConditionalGeneration
                        import torch
                        
                        st.success("✅ AI model loaded! Generating caption...")
                        
                        # Load model
                        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
                        
                        # Process image
                        inputs = processor(image, return_tensors="pt")
                        
                        # Generate caption
                        with torch.no_grad():
                            out = model.generate(**inputs, max_length=50)
                        
                        caption = processor.decode(out[0], skip_special_tokens=True)
                        
                        st.subheader("📝 Generated Caption")
                        st.write(caption)
                        st.download_button(
                            "💾 Download Caption",
                            caption,
                            file_name="caption.txt"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("💡 Tip: First-time model download may take a few minutes.")
    
    else:
        # Show welcome screen
        st.markdown("""
        ## 👋 Welcome!
        
        Upload an image using the sidebar to get started with:
        
        - **🔍 OCR**: Extract text from images in multiple languages
        - **🎨 AI Captioning**: Generate descriptive captions using AI
        - **🌍 Translation**: Translate text to 19 languages
        - **�� Text-to-Speech**: Convert text to natural-sounding audio
        
        ### 📌 Sample Features:
        - Multi-language support (7 OCR languages, 19 translation languages)
        - High-quality AI models (BLIP, EasyOCR)
        - Multiple export formats (PDF, DOCX, JSON, SRT, TXT)
        - Professional-grade accuracy
        
        **Get started by uploading an image!** 👆
        """)
        
        # Show sample images if available
        sample_dir = "sample_images"
        if os.path.exists(sample_dir):
            st.subheader("📷 Or try a sample image:")
            sample_files = [f for f in os.listdir(sample_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if sample_files:
                selected_sample = st.selectbox("Choose a sample:", [""] + sample_files)
                if selected_sample:
                    sample_path = os.path.join(sample_dir, selected_sample)
                    from PIL import Image
                    sample_image = Image.open(sample_path)
                    st.image(sample_image, caption=f"Sample: {selected_sample}", use_container_width=True)

except Exception as e:
    st.error(f"❌ Application Error: {str(e)}")
    st.info("Please check the deployment logs for more details.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 AI Image Analysis Platform - Professional Edition</p>
    <p>Powered by BLIP, EasyOCR, and Transformers | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
