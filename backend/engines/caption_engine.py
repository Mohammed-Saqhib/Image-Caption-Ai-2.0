"""
AI Caption Engine for FastAPI Backend
"""
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
import torch

class CaptionEngine:
    def __init__(self):
        """Initialize caption engine"""
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎨 Caption Engine initialized (will load model on first use, device: {self.device})")
    
    def load_model(self):
        """Load BLIP model (lazy loading)"""
        if self.model is None:
            print("Loading BLIP model...")
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model.to(self.device)
            print("✅ BLIP model loaded!")
    
    def generate_caption(self, image_path, mode="local"):
        """
        Generate caption for image
        
        Args:
            image_path: Path to image file
            mode: 'local' or 'cloud'
            
        Returns:
            dict with caption and metadata
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            if mode == "cloud":
                return self._generate_cloud(image_path)
            else:
                return self._generate_local(image)
                
        except Exception as e:
            print(f"Caption Error: {str(e)}")
            return {
                "caption": "Error generating caption",
                "confidence": 0,
                "error": str(e)
            }
    
    def _generate_local(self, image):
        """Generate caption using local model"""
        self.load_model()
        
        # Process image
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        
        # Generate caption
        outputs = self.model.generate(**inputs, max_length=50)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "caption": caption,
            "confidence": 0.90,
            "mode": "local"
        }
    
    def _generate_cloud(self, image_path):
        """Generate caption using Hugging Face API"""
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        
        with open(image_path, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, data=data)
        
        if response.status_code == 200:
            result = response.json()
            caption = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
            
            return {
                "caption": caption,
                "confidence": 0.92,
                "mode": "cloud"
            }
        else:
            raise Exception(f"API request failed: {response.status_code}")
