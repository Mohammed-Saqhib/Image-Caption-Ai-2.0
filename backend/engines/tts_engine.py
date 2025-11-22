"""
Text-to-Speech Engine for FastAPI Backend
"""
import pyttsx3
import subprocess
import platform
from pathlib import Path
import uuid

class TTSEngine:
    def __init__(self):
        """Initialize TTS engine"""
        self.system = platform.system()
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        if self.system != "Darwin":  # Not macOS
            self.engine = pyttsx3.init()
        
        print(f"🎧 TTS Engine initialized ({self.system})")
    
    def generate_speech(self, text, language="en", rate=200):
        """
        Generate speech from text
        
        Args:
            text: Text to convert to speech
            language: Language code
            rate: Speech rate (50-400)
            
        Returns:
            dict with audio file path
        """
        try:
            # Generate unique filename
            audio_file = self.output_dir / f"speech_{uuid.uuid4()}.wav"
            
            if self.system == "Darwin":  # macOS
                return self._generate_macos(text, language, rate, audio_file)
            else:
                return self._generate_pyttsx3(text, rate, audio_file)
                
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_macos(self, text, language, rate, audio_file):
        """Generate speech using macOS 'say' command"""
        # Voice mapping for different languages
        voice_map = {
            "en": "Alex",
            "hi": "Lekha",
            "ar": "Majed",
            "es": "Monica",
            "fr": "Thomas",
            "de": "Anna",
            "ja": "Kyoko",
            "ko": "Yuna",
            "zh": "Ting-Ting"
        }
        
        voice = voice_map.get(language, "Alex")
        
        # Run say command
        cmd = ["say", "-v", voice, "-r", str(rate), "-o", str(audio_file), text]
        subprocess.run(cmd, check=True)
        
        return {
            "success": True,
            "audio_file": str(audio_file),
            "voice": voice,
            "language": language
        }
    
    def _generate_pyttsx3(self, text, rate, audio_file):
        """Generate speech using pyttsx3"""
        self.engine.setProperty('rate', rate)
        self.engine.save_to_file(text, str(audio_file))
        self.engine.runAndWait()
        
        return {
            "success": True,
            "audio_file": str(audio_file),
            "engine": "pyttsx3"
        }
    
    def get_available_voices(self):
        """Get list of available voices"""
        if self.system == "Darwin":
            return [
                {"code": "en", "name": "English", "voice": "Alex"},
                {"code": "hi", "name": "Hindi", "voice": "Lekha"},
                {"code": "ar", "name": "Arabic", "voice": "Majed"},
                {"code": "es", "name": "Spanish", "voice": "Monica"},
                {"code": "fr", "name": "French", "voice": "Thomas"},
                {"code": "de", "name": "German", "voice": "Anna"},
                {"code": "ja", "name": "Japanese", "voice": "Kyoko"},
                {"code": "ko", "name": "Korean", "voice": "Yuna"}
            ]
        else:
            voices = self.engine.getProperty('voices')
            return [
                {"id": i, "name": voice.name, "lang": voice.languages}
                for i, voice in enumerate(voices)
            ]
