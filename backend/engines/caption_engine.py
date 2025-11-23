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
        """Generate caption using local model with enhanced detailed description"""
        self.load_model()
        
        # Generate basic caption with better parameters
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=50,
            num_beams=5,
            early_stopping=True
        )
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        detailed_description = caption
        
        if detailed:
            # Try to generate detailed description
            try:
                if self.detailed_model == "fallback" or self.detailed_model is None:
                    # Use BLIP-1 with enhanced prompts for detailed description
                    prompts = [
                        "Describe the scene in this image:",
                        "What objects and people can you see in this image?",
                        "What is happening in this image?",
                        "Describe the background and setting of this image:",
                        "What colors and lighting are in this image?"
                    ]
                    
                    descriptions = []
                    for prompt in prompts:
                        inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
                        outputs = self.model.generate(
                            **inputs,
                            max_length=100,
                            num_beams=5,
                            temperature=0.8,
                            do_sample=False,
                            early_stopping=True
                        )
                        desc = self.processor.decode(outputs[0], skip_special_tokens=True)
                        # Remove the prompt from the output
                        desc = desc.replace(prompt, "").strip()
                        if desc and len(desc) > 10:
                            descriptions.append(desc)
                    
                    # Combine descriptions intelligently
                    if descriptions:
                        detailed_description = self._combine_descriptions(descriptions, caption)
                    else:
                        detailed_description = self._enhance_caption(caption)
                else:
                    # Use BLIP-2 for better detailed descriptions
                    self.load_detailed_model()
                    prompt = "Question: Describe this image in detail. What objects, people, actions, colors, and background elements can you see? Answer:"
                    inputs = self.detailed_processor(image, text=prompt, return_tensors="pt").to(self.device)
                    
                    outputs = self.detailed_model.generate(
                        **inputs,
                        max_length=200,
                        min_length=50,
                        num_beams=5,
                        temperature=0.7,
                        do_sample=True,
                        top_p=0.9,
                        repetition_penalty=1.2
                    )
                    detailed_description = self.detailed_processor.decode(outputs[0], skip_special_tokens=True)
                    # Clean up the output
                    detailed_description = detailed_description.replace(prompt, "").strip()
                    if not detailed_description or len(detailed_description) < 20:
                        detailed_description = self._enhance_caption(caption)
                    
            except Exception as e:
                print(f"Detailed description generation failed: {e}, using enhanced caption")
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
        """Enhance a basic caption with more context and details"""
        # Start with a natural opening
        enhanced = f"This image shows {caption}."
        
        # Add contextual enhancements based on caption keywords
        caption_lower = caption.lower()
        
        # Subject-based enhancements
        subject_context = {
            "person": " A person is the main subject, captured in what appears to be a candid or posed photograph.",
            "people": " Multiple people are visible, suggesting a social gathering or group activity.",
            "man": " A man is prominently featured in the scene.",
            "woman": " A woman is the central figure in this image.",
            "child": " A child can be seen, adding a youthful element to the composition.",
            "children": " Children are present, bringing energy and life to the scene.",
            "baby": " A baby is visible, creating a tender moment.",
        }
        
        # Object-based enhancements
        object_context = {
            "dog": " A dog is present, likely a pet or companion animal.",
            "cat": " A cat can be seen, adding a feline presence to the image.",
            "bird": " A bird appears in the frame, possibly in flight or perched.",
            "car": " A car is visible, suggesting transportation or urban context.",
            "bicycle": " A bicycle is present, indicating cycling or outdoor activity.",
            "food": " Food items are displayed, possibly in a dining or culinary context.",
            "book": " A book is visible, suggesting reading or educational content.",
            "phone": " A phone appears, indicating modern communication or technology.",
            "computer": " A computer is present, suggesting work or digital activity.",
        }
        
        # Location-based enhancements
        location_context = {
            "beach": " The setting appears to be at a beach, with sand and possibly water visible.",
            "mountain": " Mountains can be seen in the background, suggesting a natural outdoor environment.",
            "building": " A building is visible, indicating an urban or developed area.",
            "park": " The scene takes place in a park, suggesting outdoor recreation.",
            "street": " This appears to be on a street, in an urban or suburban setting.",
            "room": " The scene is set indoors in a room.",
            "kitchen": " This takes place in a kitchen, suggesting cooking or dining activities.",
            "office": " An office setting is evident, indicating a work environment.",
        }
        
        # Activity-based enhancements
        activity_context = {
            "sitting": " The subject is in a seated position, appearing relaxed or resting.",
            "standing": " The subject is standing, suggesting an active or formal pose.",
            "walking": " Movement is captured, with someone walking through the scene.",
            "running": " Dynamic action is shown with someone running.",
            "playing": " Play or recreational activity is taking place.",
            "eating": " Dining or eating activity is captured in the moment.",
            "working": " Work-related activity is taking place.",
            "reading": " Someone is engaged in reading.",
            "smiling": " A smile is visible, suggesting happiness or positive emotion.",
        }
        
        # Weather/atmosphere enhancements
        atmosphere_context = {
            "sunny": " The lighting suggests sunny or bright conditions.",
            "cloudy": " Overcast or cloudy conditions are apparent.",
            "snow": " Snow is present, indicating winter conditions.",
            "rain": " Rain or wet conditions are visible.",
            "night": " This appears to be taken at night or in low-light conditions.",
            "sunset": " The warm lighting suggests sunset or golden hour.",
        }
        
        # Add relevant context
        context_added = False
        for keyword, context in {**subject_context, **object_context, **location_context, 
                                  **activity_context, **atmosphere_context}.items():
            if keyword in caption_lower and not context_added:
                enhanced += context
                context_added = True
                break
        
        # Add general descriptive filler if no specific context was added
        if not context_added:
            enhanced += " The composition captures various elements that tell a visual story."
        
        # Add a concluding observation
        conclusions = [
            " The image has a clear focal point and balanced composition.",
            " Various elements in the frame contribute to the overall narrative.",
            " The scene appears naturally composed with attention to detail.",
            " The photograph captures a moment in time with visual clarity.",
        ]
        
        # Select conclusion based on caption length
        conclusion_index = len(caption) % len(conclusions)
        enhanced += conclusions[conclusion_index]
        
        return enhanced
    
    def _combine_descriptions(self, descriptions, base_caption):
        """Intelligently combine multiple descriptions into a coherent narrative"""
        # Start with enhanced base caption
        combined = f"This image shows {base_caption}. "
        
        # Collect unique details from all descriptions
        all_details = []
        seen_phrases = set()
        
        for desc in descriptions:
            # Clean and normalize the description
            desc = desc.strip()
            if not desc:
                continue
                
            # Split into sentences
            sentences = desc.replace('!', '.').replace('?', '.').split('.')
            
            for sentence in sentences:
                sentence = sentence.strip()
                
                # Skip if too short or already included
                if len(sentence) < 15:
                    continue
                
                # Normalize for comparison (lowercase, remove extra spaces)
                normalized = ' '.join(sentence.lower().split())
                
                # Check if this is a new unique detail
                is_unique = True
                for seen in seen_phrases:
                    # If 70% of words overlap, consider it duplicate
                    seen_words = set(seen.split())
                    sentence_words = set(normalized.split())
                    if len(seen_words) > 0:
                        overlap = len(seen_words & sentence_words) / len(seen_words)
                        if overlap > 0.7:
                            is_unique = False
                            break
                
                if is_unique:
                    all_details.append(sentence)
                    seen_phrases.add(normalized)
        
        # Organize details by categories
        subjects = []
        actions = []
        settings = []
        colors_lighting = []
        
        for detail in all_details:
            detail_lower = detail.lower()
            
            # Categorize the detail
            if any(word in detail_lower for word in ['person', 'man', 'woman', 'child', 'people', 'someone', 'he', 'she']):
                subjects.append(detail)
            elif any(word in detail_lower for word in ['is', 'are', 'doing', 'holding', 'wearing', 'standing', 'sitting', 'walking']):
                actions.append(detail)
            elif any(word in detail_lower for word in ['background', 'setting', 'location', 'scene', 'place', 'area']):
                settings.append(detail)
            elif any(word in detail_lower for word in ['color', 'light', 'bright', 'dark', 'shadow', 'sun', 'sky']):
                colors_lighting.append(detail)
            else:
                # Default to action if unclear
                actions.append(detail)
        
        # Build narrative structure
        narrative_parts = []
        
        # Add subject information
        if subjects:
            narrative_parts.append(subjects[0])
        
        # Add action information
        if actions:
            narrative_parts.append(actions[0])
            if len(actions) > 1:
                narrative_parts.append(actions[1])
        
        # Add setting/background
        if settings:
            narrative_parts.append(settings[0])
        
        # Add color/lighting if available
        if colors_lighting:
            narrative_parts.append(colors_lighting[0])
        
        # Combine narrative parts
        if narrative_parts:
            combined += " ".join(narrative_parts[:4])  # Limit to 4 most relevant details
            if not combined.endswith('.'):
                combined += '.'
        else:
            # Fallback: use first 3 unique details
            if all_details:
                combined += " ".join(all_details[:3])
                if not combined.endswith('.'):
                    combined += '.'
        
        return combined
