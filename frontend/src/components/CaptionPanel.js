import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaImage, FaDownload, FaCopy, FaCheck, FaCloud, FaLaptop } from 'react-icons/fa';
import './CaptionPanel.css';

const CaptionPanel = ({ onProcess, result, loading, hasImage }) => {
  const [mode, setMode] = useState('cloud');
  const [copied, setCopied] = useState(false);

  const handleGenerate = () => {
    onProcess(mode);
  };

  const copyToClipboard = () => {
    if (result?.data?.caption) {
      navigator.clipboard.writeText(result.data.caption);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const downloadCaption = () => {
    if (result?.data?.caption) {
      const blob = new Blob([result.data.caption], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai_caption_${Date.now()}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <motion.div
      className="panel caption-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="panel-header">
        <FaImage className="panel-icon" />
        <h2>AI Image Captioning</h2>
        <p>Generate natural language descriptions using BLIP AI</p>
      </div>

      <div className="panel-content">
        {!hasImage ? (
          <motion.div
            className="no-image-state"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
          >
            <FaImage className="no-image-icon" />
            <h3>No Image Uploaded</h3>
            <p>Please upload an image from the left sidebar to generate AI-powered captions</p>
          </motion.div>
        ) : (
          <>
            <div className="mode-selector">
              <h3>Processing Mode</h3>
              <div className="mode-options">
                <motion.button
                  className={`mode-btn ${mode === 'cloud' ? 'selected' : ''}`}
                  onClick={() => setMode('cloud')}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaCloud />
                  <div>
                    <strong>Cloud Mode</strong>
                    <span>Faster, uses Hugging Face API</span>
                  </div>
            </motion.button>

            <motion.button
              className={`mode-btn ${mode === 'local' ? 'selected' : ''}`}
              onClick={() => setMode('local')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaLaptop />
              <div>
                <strong>Local Mode</strong>
                <span>More privacy, runs on server</span>
              </div>
            </motion.button>
          </div>
        </div>

        <motion.button
          className="action-btn primary"
          onClick={handleGenerate}
          disabled={loading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Generating Caption...
            </>
          ) : (
            <>
              <FaImage /> Generate Caption
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
              <h3>AI Generated Caption</h3>
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
                  onClick={downloadCaption}
                  title="Download as TXT"
                >
                  <FaDownload />
                </button>
              </div>
            </div>

            <div className="result-stats">
              <div className="stat">
                <span className="stat-label">Model:</span>
                <span className="stat-value">BLIP</span>
              </div>
              <div className="stat">
                <span className="stat-label">Mode:</span>
                <span className="stat-value">{result.data.mode}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Confidence:</span>
                <span className="stat-value">{(result.data.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>

            <div className="caption-display">
              <div className="caption-icon">💬</div>
              <div className="caption-content">
                <div className="caption-section">
                  <h4>Quick Caption</h4>
                  <p className="caption-text">{result.data.caption}</p>
                </div>
                
                {result.data.detailed_description && result.data.detailed_description !== result.data.caption && (
                  <div className="caption-section detailed">
                    <h4>📝 Detailed Description</h4>
                    <p className="detailed-text">{result.data.detailed_description}</p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
          </>
        )}
      </div>
    </motion.div>
  );
};

export default CaptionPanel;
