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
        Extract text from image file with proper left-to-right, top-to-bottom ordering
        
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
            
            # Extract text with bounding boxes
            results = reader.readtext(image_np)
            
            if not results:
                return {
                    "text": "",
                    "languages": languages,
                    "confidence": 0,
                    "detections": 0
                }
            
            # Sort results by position (top-to-bottom, left-to-right)
            # First, sort by y-coordinate (top to bottom) with tolerance for same line
            # Then sort by x-coordinate (left to right)
            sorted_results = self._sort_text_by_position(results)
            
            # Combine text in proper reading order
            extracted_text = " ".join([text for (bbox, text, conf) in sorted_results])
            
            # Calculate average confidence
            avg_confidence = sum([conf for (bbox, text, conf) in sorted_results]) / len(sorted_results)
            
            return {
                "text": extracted_text,
                "languages": languages,
                "confidence": round(avg_confidence, 2),
                "detections": len(sorted_results),
                "reading_order": "left-to-right, top-to-bottom"
            }
            
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            return {
                "text": "",
                "languages": languages,
                "confidence": 0,
                "error": str(e)
            }
    
    def _sort_text_by_position(self, results):
        """
        Sort text results by reading order (top-to-bottom, left-to-right)
        
        Args:
            results: List of (bbox, text, confidence) tuples from EasyOCR
            
        Returns:
            Sorted list in reading order
        """
        # Group results by rows (with tolerance for slight vertical differences)
        rows = []
        line_tolerance = 20  # pixels tolerance for same line
        
        for bbox, text, conf in results:
            # Get center y-coordinate of bounding box
            y_coords = [point[1] for point in bbox]
            y_center = sum(y_coords) / len(y_coords)
            
            # Get leftmost x-coordinate
            x_coords = [point[0] for point in bbox]
            x_left = min(x_coords)
            
            # Find or create row
            found_row = False
            for row in rows:
                row_y = row['y']
                if abs(y_center - row_y) < line_tolerance:
                    row['items'].append((x_left, bbox, text, conf))
                    found_row = True
                    break
            
            if not found_row:
                rows.append({
                    'y': y_center,
                    'items': [(x_left, bbox, text, conf)]
                })
        
        # Sort rows by y-coordinate (top to bottom)
        rows.sort(key=lambda r: r['y'])
        
        # Sort items within each row by x-coordinate (left to right)
        sorted_results = []
        for row in rows:
            row['items'].sort(key=lambda item: item[0])  # Sort by x_left
            # Add to results (remove x_left coordinate)
            sorted_results.extend([(bbox, text, conf) for x, bbox, text, conf in row['items']])
        
        return sorted_results
