import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

import ImageUpload from './components/ImageUpload';
import OCRPanel from './components/OCRPanel';
import CaptionPanel from './components/CaptionPanel';
import TranslationPanel from './components/TranslationPanel';
import TTSPanel from './components/TTSPanel';
import Header from './components/Header';
import TabNavigation from './components/TabNavigation';

import * as api from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('ocr');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Results
  const [ocrResult, setOcrResult] = useState(null);
  const [captionResult, setCaptionResult] = useState(null);
  const [translationResult, setTranslationResult] = useState(null);
  
  // Health check on mount
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const health = await api.healthCheck();
      console.log('API Health:', health);
      toast.success('✅ Connected to API successfully!', {
        position: 'bottom-right',
        autoClose: 3000,
      });
    } catch (error) {
      console.error('API Health Check Failed:', error);
      toast.error('⚠️ Could not connect to API. Check backend status.', {
        position: 'bottom-right',
        autoClose: 5000,
      });
    }
  };

  const handleImageUpload = (file) => {
    setUploadedImage(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
    
    toast.info('📸 Image uploaded! Select a feature to process.', {
      position: 'top-center',
      autoClose: 2000,
    });
  };

  const handleOCR = async (languages) => {
    if (!uploadedImage) {
      toast.warn('Please upload an image first!');
      return;
    }

    setLoading(true);
    try {
      const result = await api.extractText(uploadedImage, languages.join(','));
      setOcrResult(result);
      setActiveTab('ocr');
      toast.success('✅ Text extracted successfully!');
    } catch (error) {
      console.error('OCR Error:', error);
      toast.error('❌ Failed to extract text. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCaption = async (mode) => {
    if (!uploadedImage) {
      toast.warn('Please upload an image first!');
      return;
    }

    setLoading(true);
    try {
      const result = await api.generateCaption(uploadedImage, mode);
      setCaptionResult(result);
      setActiveTab('caption');
      toast.success('✅ Caption generated successfully!');
    } catch (error) {
      console.error('Caption Error:', error);
      toast.error('❌ Failed to generate caption. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async (text, targetLanguage) => {
    if (!text) {
      toast.warn('Please enter text to translate!');
      return;
    }

    setLoading(true);
    try {
      const result = await api.translateText(text, targetLanguage);
      setTranslationResult(result);
      toast.success('✅ Text translated successfully!');
    } catch (error) {
      console.error('Translation Error:', error);
      toast.error('❌ Failed to translate text. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTTS = async (text, language, rate) => {
    if (!text) {
      toast.warn('Please enter text for speech!');
      return;
    }

    setLoading(true);
    try {
      const audioBlob = await api.textToSpeech(text, language, rate);
      const audioUrl = URL.createObjectURL(audioBlob);
      
      // Play audio
      const audio = new Audio(audioUrl);
      audio.play();
      
      toast.success('🎧 Playing audio...');
    } catch (error) {
      console.error('TTS Error:', error);
      toast.error('❌ Failed to generate speech. Try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      
      <motion.div
        className="container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <ImageUpload
          onUpload={handleImageUpload}
          imagePreview={imagePreview}
          loading={loading}
        />

        <TabNavigation
          activeTab={activeTab}
          setActiveTab={setActiveTab}
        />

        <div className="content-panels">
          {activeTab === 'ocr' && (
            <OCRPanel
              onProcess={handleOCR}
              result={ocrResult}
              loading={loading}
            />
          )}

          {activeTab === 'caption' && (
            <CaptionPanel
              onProcess={handleCaption}
              result={captionResult}
              loading={loading}
            />
          )}

          {activeTab === 'translation' && (
            <TranslationPanel
              onTranslate={handleTranslate}
              result={translationResult}
              loading={loading}
              ocrText={ocrResult?.data?.text}
              captionText={captionResult?.data?.caption}
            />
          )}

          {activeTab === 'tts' && (
            <TTSPanel
              onGenerate={handleTTS}
              loading={loading}
              ocrText={ocrResult?.data?.text}
              captionText={captionResult?.data?.caption}
              translatedText={translationResult?.data?.translated_text}
            />
          )}
        </div>
      </motion.div>

      <ToastContainer
        position="bottom-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </div>
  );
}

export default App;
