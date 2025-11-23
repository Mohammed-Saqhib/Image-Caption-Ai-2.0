"""
AI Caption Engine for FastAPI Backend with Detailed Descriptions
"""
from transformers import BlipProcessor, BlipForConditionalGeneration, Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import requests
import torch

class CaptionEngine:
    def __init__(self):
        """Initialize caption engine"""
        self.model = None
        self.processor = None
        self.detailed_model = None
        self.detailed_processor = None
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
    
    def load_detailed_model(self):
        """Load BLIP-2 model for detailed descriptions"""
        if self.detailed_model is None:
            print("Loading BLIP-2 model for detailed descriptions...")
            try:
                self.detailed_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
                self.detailed_model = Blip2ForConditionalGeneration.from_pretrained(
                    "Salesforce/blip2-opt-2.7b",
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                self.detailed_model.to(self.device)
                print("✅ BLIP-2 detailed model loaded!")
            except Exception as e:
                print(f"⚠️ BLIP-2 model failed to load: {e}")
                print("   Falling back to BLIP-1 with enhanced prompts")
                self.detailed_model = "fallback"
    
    def generate_caption(self, image_path, mode="local", detailed=True):
        """
        Generate caption for image with optional detailed description
        
        Args:
            image_path: Path to image file
            mode: 'local' or 'cloud'
            detailed: If True, generate detailed description
            
        Returns:
            dict with caption, detailed description, and metadata
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            if mode == "cloud":
                result = self._generate_cloud(image_path, detailed)
            else:
                result = self._generate_local(image, detailed)
            
            return result
                
        except Exception as e:
            print(f"Caption Error: {str(e)}")
            return {
                "caption": "Error generating caption",
                "detailed_description": "Error generating description",
                "confidence": 0,
                "error": str(e)
            }
    
    def _generate_local(self, image, detailed=True):
        """Generate caption using local model with detailed description"""
        self.load_model()
        
        # Generate basic caption
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_length=50)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        detailed_description = caption
        
        if detailed:
            # Try to generate detailed description
            try:
                if self.detailed_model == "fallback" or self.detailed_model is None:
                    # Use BLIP-1 with specific prompts for detailed description
                    prompts = [
                        "Describe this image in detail:",
                        "What is happening in this image?",
                        "Describe the scene, people, objects, and background:"
                    ]
                    
                    descriptions = []
                    for prompt in prompts:
                        inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
                        outputs = self.model.generate(**inputs, max_length=100, num_beams=5)
                        desc = self.processor.decode(outputs[0], skip_special_tokens=True)
                        # Remove the prompt from the output
                        desc = desc.replace(prompt, "").strip()
                        if desc and len(desc) > 10:
                            descriptions.append(desc)
                    
                    # Combine descriptions intelligently
                    if descriptions:
                        detailed_description = self._combine_descriptions(descriptions, caption)
                else:
                    # Use BLIP-2 for better detailed descriptions
                    self.load_detailed_model()
                    prompt = "Describe this image in detail. What objects, people, actions, and background elements can you see?"
                    inputs = self.detailed_processor(image, text=prompt, return_tensors="pt").to(self.device)
                    
                    outputs = self.detailed_model.generate(
                        **inputs,
                        max_length=150,
                        num_beams=5,
                        temperature=0.7,
                        do_sample=True
                    )
                    detailed_description = self.detailed_processor.decode(outputs[0], skip_special_tokens=True)
                    
            except Exception as e:
                print(f"Detailed description generation failed: {e}, using basic caption")
                detailed_description = self._enhance_caption(caption)
        
        return {
            "caption": caption,
            "detailed_description": detailed_description,
            "confidence": 0.90,
            "mode": "local",
            "has_detailed": detailed
        }
    
    def _generate_cloud(self, image_path, detailed=True):
        """Generate caption using Hugging Face API"""
        # Basic caption
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        
        with open(image_path, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, data=data)
        
        caption = ""
        if response.status_code == 200:
            result = response.json()
            caption = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
        else:
            raise Exception(f"API request failed: {response.status_code}")
        
        detailed_description = caption
        
        # Try to get detailed description
        if detailed:
            try:
                # Use BLIP-2 for detailed description
                DETAILED_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b"
                
                # Send with prompt
                import json
                payload = {
                    "inputs": "Describe this image in detail, including people, objects, actions, background, and setting:"
                }
                
                response = requests.post(
                    DETAILED_API_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    files={"file": open(image_path, "rb")}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        detailed_description = result[0].get("generated_text", caption)
                    else:
                        detailed_description = self._enhance_caption(caption)
                else:
                    detailed_description = self._enhance_caption(caption)
                    
            except Exception as e:
                print(f"Detailed cloud description failed: {e}")
                detailed_description = self._enhance_caption(caption)
        
        return {
            "caption": caption,
            "detailed_description": detailed_description,
            "confidence": 0.92,
            "mode": "cloud",
            "has_detailed": detailed
        }
    
    def _enhance_caption(self, caption):
        """Enhance a basic caption with more context"""
        # Add contextual enhancements
        enhanced = f"The image shows {caption}."
        
        # Add common scene elements based on caption keywords
        keywords_context = {
            "person": " The person appears to be the main subject of the image.",
            "people": " Multiple people are visible in the scene.",
            "man": " A man is present in the scene.",
            "woman": " A woman is present in the scene.",
            "child": " A child can be seen in the image.",
            "dog": " A dog is visible in the photograph.",
            "cat": " A cat can be seen in the image.",
            "beach": " The setting appears to be at a beach.",
            "mountain": " Mountains can be seen in the background.",
            "building": " A building is visible in the scene.",
            "car": " A car is present in the image.",
            "food": " Food items are displayed in the image.",
            "outdoor": " This appears to be an outdoor scene.",
            "indoor": " This appears to be an indoor scene.",
        }
        
        caption_lower = caption.lower()
        for keyword, context in keywords_context.items():
            if keyword in caption_lower:
                enhanced += context
        
        return enhanced
    
    def _combine_descriptions(self, descriptions, base_caption):
        """Intelligently combine multiple descriptions"""
        # Start with base caption
        combined = f"The image shows {base_caption}. "
        
        # Add unique details from descriptions
        unique_details = set()
        for desc in descriptions:
            # Split into sentences
            sentences = desc.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and len(sentence) > 15:
                    unique_details.add(sentence)
        
        # Combine unique details
        if unique_details:
            combined += " ".join(list(unique_details)[:3]) + "."
        
        return combined
