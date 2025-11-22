"""
Translation Engine for FastAPI Backend
"""
from deep_translator import GoogleTranslator

class TranslationEngine:
    def __init__(self):
        """Initialize translation engine"""
        self.supported_languages = {
            "en": "English",
            "hi": "Hindi",
            "ar": "Arabic",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-CN": "Chinese (Simplified)",
            "ru": "Russian",
            "ta": "Tamil",
            "te": "Telugu",
            "bn": "Bengali",
            "mr": "Marathi",
            "gu": "Gujarati",
            "kn": "Kannada",
            "ml": "Malayalam"
        }
        print("🌍 Translation Engine initialized")
    
    def translate(self, text, target_language, source_language="auto"):
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect by default)
            
        Returns:
            dict with translated text
        """
        try:
            translator = GoogleTranslator(source=source_language, target=target_language)
            translated_text = translator.translate(text)
            
            return {
                "translated_text": translated_text,
                "source_language": source_language,
                "target_language": target_language
            }
            
        except Exception as e:
            print(f"Translation Error: {str(e)}")
            return {
                "translated_text": text,
                "error": str(e)
            }
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return [
            {"code": code, "name": name}
            for code, name in self.supported_languages.items()
        ]
