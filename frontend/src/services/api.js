/**
 * API Service for AI Image Analysis Platform
 */
import axios from 'axios';

// API Base URL - Change this to your Hugging Face Space URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

/**
 * OCR - Extract text from image
 */
export const extractText = async (file, languages = 'en') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('languages', languages);

  const response = await api.post('/api/ocr', formData);
  return response.data;
};

/**
 * AI Caption - Generate caption for image
 */
export const generateCaption = async (file, mode = 'cloud') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('mode', mode);

  const response = await api.post('/api/caption', formData);
  return response.data;
};

/**
 * Translation - Translate text
 */
export const translateText = async (text, targetLanguage) => {
  const response = await api.post('/api/translate', {
    text,
    target_language: targetLanguage,
  }, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};

/**
 * Text-to-Speech - Convert text to speech
 */
export const textToSpeech = async (text, language = 'en', rate = 200) => {
  try {
    console.log('TTS Request:', { text: text.substring(0, 50), language, rate });
    const response = await api.post('/api/tts', {
      text,
      language,
      rate,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      responseType: 'blob',
    });
    console.log('TTS Response:', response.status, response.headers['content-type'], 'size:', response.data.size);
    return response.data;
  } catch (error) {
    console.error('TTS API Error:', {
      message: error.message,
      response: error.response?.status,
      data: error.response?.data
    });
    throw error;
  }
};

/**
 * Get supported OCR languages
 */
export const getOCRLanguages = async () => {
  const response = await api.get('/api/languages/ocr');
  return response.data;
};

/**
 * Get supported translation languages
 */
export const getTranslationLanguages = async () => {
  const response = await api.get('/api/languages/translation');
  return response.data;
};

/**
 * Get available TTS voices
 */
export const getAvailableVoices = async () => {
  const response = await api.get('/api/voices');
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

const apiExports = {
  extractText,
  generateCaption,
  translateText,
  textToSpeech,
  getOCRLanguages,
  getTranslationLanguages,
  getAvailableVoices,
  healthCheck
};

export default apiExports;
