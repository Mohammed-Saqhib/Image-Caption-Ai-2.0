"""
OCR Engine for FastAPI Backend
"""
import easyocr
import numpy as np
from PIL import Image
from pathlib import Path

class OCREngine:
    def __init__(self):
        """Initialize OCR engine with default languages"""
        self.readers = {}
        print("📸 OCR Engine initialized (readers created on demand)")
    
    def get_reader(self, languages):
        """Get or create reader for specified languages"""
        lang_key = ','.join(sorted(languages))
        
        if lang_key not in self.readers:
            print(f"Creating EasyOCR reader for: {languages}")
            self.readers[lang_key] = easyocr.Reader(languages, gpu=False)
        
        return self.readers[lang_key]
    
    def extract_text(self, image_path, languages=['en']):
        """
        Extract text from image file
        
        Args:
            image_path: Path to image file
            languages: List of language codes
            
        Returns:
            dict with extracted text and metadata
        """
        try:
            # Load image
            image = Image.open(image_path)
            image_np = np.array(image)
            
            # Get reader for languages
            reader = self.get_reader(languages)
            
            # Extract text
            results = reader.readtext(image_np)
            
            # Combine all text
            extracted_text = " ".join([text for (bbox, text, conf) in results])
            
            # Calculate average confidence
            avg_confidence = sum([conf for (bbox, text, conf) in results]) / len(results) if results else 0
            
            return {
                "text": extracted_text,
                "languages": languages,
                "confidence": round(avg_confidence, 2),
                "detections": len(results)
            }
            
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            return {
                "text": "",
                "languages": languages,
                "confidence": 0,
                "error": str(e)
            }
