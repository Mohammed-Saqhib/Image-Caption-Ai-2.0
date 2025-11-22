import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaLanguage, FaDownload, FaCopy, FaCheck } from 'react-icons/fa';
import * as api from '../services/api';
import './TranslationPanel.css';

const TranslationPanel = ({ onTranslate, result, loading, ocrText, captionText }) => {
  const [sourceText, setSourceText] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('es');
  const [availableLanguages, setAvailableLanguages] = useState([]);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadLanguages();
  }, []);

  useEffect(() => {
    // Auto-populate with OCR text if available
    if (ocrText && !sourceText) {
      setSourceText(ocrText);
    } else if (captionText && !sourceText) {
      setSourceText(captionText);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ocrText, captionText]);

  const loadLanguages = async () => {
    try {
      const data = await api.getTranslationLanguages();
      setAvailableLanguages(data.languages || []);
    } catch (error) {
      console.error('Failed to load languages:', error);
    }
  };

  const handleTranslate = () => {
    if (sourceText.trim()) {
      onTranslate(sourceText, targetLanguage);
    }
  };

  const useOCRText = () => {
    if (ocrText) setSourceText(ocrText);
  };

  const useCaptionText = () => {
    if (captionText) setSourceText(captionText);
  };

  const copyToClipboard = () => {
    if (result?.data?.translated_text) {
      navigator.clipboard.writeText(result.data.translated_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const downloadTranslation = () => {
    if (result?.data?.translated_text) {
      const content = `Original:\n${result.data.original_text}\n\nTranslated (${result.data.target_language}):\n${result.data.translated_text}`;
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `translation_${Date.now()}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <motion.div
      className="panel translation-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="panel-header">
        <FaLanguage className="panel-icon" />
        <h2>Multi-Language Translation</h2>
        <p>Translate text to 19+ languages using Google Translator</p>
      </div>

      <div className="panel-content">
        <div className="text-input-section">
          <div className="input-header">
            <h3>Source Text</h3>
            <div className="quick-actions">
              {ocrText && (
                <button className="quick-btn" onClick={useOCRText}>
                  Use OCR Text
                </button>
              )}
              {captionText && (
                <button className="quick-btn" onClick={useCaptionText}>
                  Use Caption
                </button>
              )}
            </div>
          </div>
          <textarea
            className="text-input"
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            placeholder="Enter text to translate or use OCR/Caption text..."
            rows={6}
          />
        </div>

        <div className="language-selector">
          <h3>Target Language</h3>
          <select
            className="language-select"
            value={targetLanguage}
            onChange={(e) => setTargetLanguage(e.target.value)}
          >
            {availableLanguages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        <motion.button
          className="action-btn primary"
          onClick={handleTranslate}
          disabled={loading || !sourceText.trim()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Translating...
            </>
          ) : (
            <>
              <FaLanguage /> Translate
            </>
          )}
        </motion.button>

        {result && result.success && (
          <motion.div
            className="result-box"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="result-header">
              <h3>Translation Result</h3>
              <div className="result-actions">
                <button
                  className="icon-btn"
                  onClick={copyToClipboard}
                  title="Copy to clipboard"
                >
                  {copied ? <FaCheck /> : <FaCopy />}
                </button>
                <button
                  className="icon-btn"
                  onClick={downloadTranslation}
                  title="Download as TXT"
                >
                  <FaDownload />
                </button>
              </div>
            </div>

            <div className="translation-display">
              <div className="translation-box">
                <div className="translation-label">Original</div>
                <p>{result.data.original_text}</p>
              </div>
              <div className="translation-arrow">→</div>
              <div className="translation-box highlight">
                <div className="translation-label">Translated</div>
                <p>{result.data.translated_text}</p>
              </div>
            </div>

            <div className="result-stats">
              <div className="stat">
                <span className="stat-label">Target Language:</span>
                <span className="stat-value">{result.data.target_language}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Word Count:</span>
                <span className="stat-value">{result.data.word_count}</span>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default TranslationPanel;
