"""
📦 Pydantic Models for Request/Response Validation
Comprehensive data models for type safety and validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class CaptionMode(str, Enum):
    """Caption generation modes"""
    LOCAL = "local"
    CLOUD = "cloud"


class LanguageCode(str, Enum):
    """Supported language codes"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    HINDI = "hi"
    TURKISH = "tr"
    DUTCH = "nl"
    POLISH = "pl"
    SWEDISH = "sv"
    DANISH = "da"
    NORWEGIAN = "no"
    FINNISH = "fi"


# ============ Request Models ============

class OCRRequest(BaseModel):
    """OCR processing request"""
    languages: List[str] = Field(
        default=["en"],
        description="List of language codes for OCR",
        min_items=1,
        max_items=5
    )


class CaptionRequest(BaseModel):
    """Image captioning request"""
    mode: CaptionMode = Field(
        default=CaptionMode.LOCAL,
        description="Caption generation mode (local or cloud)"
    )


class TranslationRequest(BaseModel):
    """Translation request"""
    text: str = Field(
        ...,
        description="Text to translate",
        min_length=1,
        max_length=5000
    )
    target_language: str = Field(
        ...,
        description="Target language code",
        min_length=2,
        max_length=5
    )
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()


class TTSRequest(BaseModel):
    """Text-to-speech request"""
    text: str = Field(
        ...,
        description="Text to convert to speech",
        min_length=1,
        max_length=1000
    )
    voice: str = Field(
        default="default",
        description="Voice selection"
    )
    rate: int = Field(
        default=150,
        description="Speech rate (words per minute)",
        ge=50,
        le=300
    )
    volume: float = Field(
        default=1.0,
        description="Volume level",
        ge=0.0,
        le=1.0
    )


# ============ Response Models ============

class OCRResponse(BaseModel):
    """OCR processing response"""
    success: bool
    text: str
    languages: List[str]
    confidence: Optional[float] = None
    word_count: int
    char_count: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)


class CaptionResponse(BaseModel):
    """Image captioning response"""
    success: bool
    caption: str
    mode: str
    confidence: Optional[float] = None
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)


class TranslationResponse(BaseModel):
    """Translation response"""
    success: bool
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    char_count: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)


class TTSResponse(BaseModel):
    """Text-to-speech response"""
    success: bool
    audio_url: str
    text: str
    voice: str
    duration: Optional[float] = None
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)


class LanguageInfo(BaseModel):
    """Language information"""
    code: str
    name: str
    native_name: str
    supported_features: List[str]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    uptime: float
    engines: Dict[str, str]
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    error_code: str
    timestamp: datetime = Field(default_factory=datetime.now)
    path: Optional[str] = None


class BatchOCRRequest(BaseModel):
    """Batch OCR request"""
    languages: List[str] = Field(
        default=["en"],
        description="List of language codes",
        max_items=5
    )
    max_images: int = Field(
        default=10,
        description="Maximum images to process",
        ge=1,
        le=50
    )


class BatchOCRResponse(BaseModel):
    """Batch OCR response"""
    success: bool
    results: List[OCRResponse]
    total_processed: int
    total_failed: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)


# ============ Stats Models ============

class UsageStats(BaseModel):
    """API usage statistics"""
    total_requests: int
    ocr_requests: int
    caption_requests: int
    translation_requests: int
    tts_requests: int
    average_processing_time: float
    total_images_processed: int
    total_characters_processed: int
    uptime: float


class FileValidation(BaseModel):
    """File validation result"""
    is_valid: bool
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    error: Optional[str] = None
