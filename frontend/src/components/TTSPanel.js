import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaVolumeUp, FaPlay, FaPause, FaDownload } from 'react-icons/fa';
import * as api from '../services/api';
import './TTSPanel.css';

const TTSPanel = ({ onGenerate, loading, ocrText, captionText, translatedText }) => {
  const [sourceText, setSourceText] = useState('');
  const [language, setLanguage] = useState('en');
  const [rate, setRate] = useState(200);
  const [availableVoices, setAvailableVoices] = useState([]);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = React.useRef(null);

  useEffect(() => {
    loadVoices();
    
    // Cleanup function
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    // Auto-populate with available text
    if (translatedText && !sourceText) {
      setSourceText(translatedText);
    } else if (ocrText && !sourceText) {
      setSourceText(ocrText);
    } else if (captionText && !sourceText) {
      setSourceText(captionText);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ocrText, captionText, translatedText]);

  const loadVoices = async () => {
    try {
      const data = await api.getAvailableVoices();
      setAvailableVoices(data.voices || []);
    } catch (error) {
      console.error('Failed to load voices:', error);
    }
  };

  const handleGenerate = async () => {
    if (!sourceText.trim()) {
      return;
    }
    
    try {
      setIsPlaying(false);
      
      // Clear old URL
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
        setAudioUrl(null);
      }
      
      // Call the parent's onGenerate handler if provided, otherwise handle internally
      if (onGenerate) {
        const audioBlob = await onGenerate(sourceText, language, rate);
        if (audioBlob && audioBlob instanceof Blob) {
          console.log('Received audio blob:', audioBlob.size, 'bytes', audioBlob.type);
          const url = URL.createObjectURL(audioBlob);
          setAudioUrl(url);
          console.log('Audio URL created:', url);
          // Don't autoplay - let user click play button
        } else {
          console.error('Invalid audio blob received:', audioBlob);
        }
      } else {
        const audioBlob = await api.textToSpeech(sourceText, language, rate);
        if (audioBlob && audioBlob instanceof Blob) {
          console.log('Received audio blob:', audioBlob.size, 'bytes', audioBlob.type);
          const url = URL.createObjectURL(audioBlob);
          setAudioUrl(url);
          console.log('Audio URL created:', url);
          // Don't autoplay - let user click play button
        } else {
          console.error('Invalid audio blob received:', audioBlob);
          throw new Error('Failed to receive audio data');
        }
      }
    } catch (error) {
      console.error('TTS Error in handleGenerate:', error);
      setIsPlaying(false);
      // Error will be shown by toast in parent component
      throw error; // Re-throw so parent can handle it
    }
  };

  const togglePlayPause = () => {
    const audio = audioRef.current;
    
    if (!audio || !audioUrl) {
      console.log('No audio available');
      return;
    }
    
    console.log('Audio state:', { 
      isPlaying, 
      paused: audio.paused, 
      src: audio.src,
      readyState: audio.readyState 
    });
    
    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      // Ensure the audio source is set
      if (!audio.src || audio.src === '') {
        audio.src = audioUrl;
      }
      
      const playPromise = audio.play();
      
      if (playPromise !== undefined) {
        playPromise.then(() => {
          console.log('Playback started successfully');
          setIsPlaying(true);
        }).catch((error) => {
          console.error('Playback error:', error);
          setIsPlaying(false);
          
          // Try to reload and play again
          audio.load();
          setTimeout(() => {
            audio.play().then(() => {
              setIsPlaying(true);
            }).catch(err => {
              console.error('Retry failed:', err);
            });
          }, 100);
        });
      }
    }
  };

  const downloadAudio = () => {
    if (audioUrl) {
      const a = document.createElement('a');
      a.href = audioUrl;
      a.download = `speech_${Date.now()}.wav`;
      a.click();
    }
  };

  const useOCRText = () => {
    if (ocrText) setSourceText(ocrText);
  };

  const useCaptionText = () => {
    if (captionText) setSourceText(captionText);
  };

  const useTranslatedText = () => {
    if (translatedText) setSourceText(translatedText);
  };

  return (
    <motion.div
      className="panel tts-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="panel-header">
        <FaVolumeUp className="panel-icon" />
        <h2>Text-to-Speech</h2>
        <p>Convert text to natural-sounding audio in multiple languages</p>
      </div>

      <div className="panel-content">
        {/* Hidden audio element */}
        <audio 
          ref={audioRef} 
          src={audioUrl || ''} 
          preload="auto"
          onLoadedData={() => console.log('Audio loaded and ready')}
          onCanPlayThrough={() => console.log('Audio can play through')}
          onEnded={() => setIsPlaying(false)}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onError={(e) => {
            console.error('Audio error:', e);
            setIsPlaying(false);
          }}
          style={{ display: 'none' }}
        />
        
        <div className="text-input-section">
          <div className="input-header">
            <h3>Text to Convert</h3>
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
              {translatedText && (
                <button className="quick-btn" onClick={useTranslatedText}>
                  Use Translation
                </button>
              )}
            </div>
          </div>
          <textarea
            className="text-input"
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            placeholder="Enter text to convert to speech or use OCR/Caption/Translation text..."
            rows={6}
          />
        </div>

        <div className="tts-controls">
          <div className="control-group">
            <label>Voice Language</label>
            <select
              className="control-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              {availableVoices.map((voice, idx) => (
                <option key={idx} value={voice.code}>
                  {voice.name} {voice.voice && `(${voice.voice})`}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group">
            <label>Speech Rate: {rate}</label>
            <input
              type="range"
              className="control-slider"
              min="50"
              max="400"
              value={rate}
              onChange={(e) => setRate(parseInt(e.target.value))}
            />
            <div className="slider-labels">
              <span>Slow</span>
              <span>Normal</span>
              <span>Fast</span>
            </div>
          </div>
        </div>

        <motion.button
          className="action-btn primary"
          onClick={handleGenerate}
          disabled={loading || !sourceText.trim()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Generating Speech...
            </>
          ) : (
            <>
              <FaVolumeUp /> Generate Speech
            </>
          )}
        </motion.button>

        {audioUrl && (
          <motion.div
            className="audio-player"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="player-header">
              <h3>🎧 Audio Player</h3>
              <button
                className="icon-btn"
                onClick={downloadAudio}
                title="Download Audio"
              >
                <FaDownload />
              </button>
            </div>

            <div className="player-controls">
              <motion.button
                className="play-btn"
                onClick={togglePlayPause}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                {isPlaying ? <FaPause /> : <FaPlay />}
              </motion.button>
              <div className="audio-info">
                <div className="audio-waveform">
                  {[...Array(30)].map((_, i) => (
                    <div
                      key={i}
                      className={`wave-bar ${isPlaying ? 'active' : ''}`}
                      style={{ animationDelay: `${i * 0.05}s` }}
                    />
                  ))}
                </div>
                <p className="audio-status">
                  {isPlaying ? 'Playing...' : 'Ready to play'}
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default TTSPanel;
