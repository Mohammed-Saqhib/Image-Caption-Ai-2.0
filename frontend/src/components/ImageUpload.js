import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { FaCloudUploadAlt, FaImage, FaImages } from 'react-icons/fa';
import { sampleImages, loadSampleImage } from '../data/sampleImages';
import './ImageUpload.css';

const ImageUpload = ({ onUpload, imagePreview, loading }) => {
  const [showSamples, setShowSamples] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
      setShowSamples(false);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    },
    multiple: false,
    disabled: loading
  });

  const handleSampleSelect = async (sample) => {
    const file = await loadSampleImage(sample.path);
    if (file) {
      onUpload(file);
      setShowSamples(false);
    }
  };

  return (
    <motion.div
      className="image-upload-container"
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div
        {...getRootProps()}
        className={`upload-area ${isDragActive ? 'drag-active' : ''} ${loading ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />
        
        {imagePreview ? (
          <div className="upload-success">
            <div className="success-icon">✓</div>
            <h3>Image Uploaded!</h3>
            <p>Click to change image</p>
            <div className="success-badge">Ready to Process</div>
          </div>
        ) : (
          <div className="upload-prompt">
            <FaCloudUploadAlt className="upload-icon" />
            <h3>Upload Image</h3>
            <p>Drag & drop or click to browse</p>
            <span className="file-types">PNG, JPG, JPEG, GIF, WEBP</span>
          </div>
        )}
      </div>

      {/* Sample Images Button */}
      <motion.button
        className="sample-images-toggle"
        onClick={() => setShowSamples(!showSamples)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        disabled={loading}
      >
        <FaImages /> {showSamples ? 'Hide' : 'Show'} Sample Images
      </motion.button>

      {/* Sample Images Grid */}
      <AnimatePresence>
        {showSamples && (
          <motion.div
            className="sample-images-grid"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h4 className="samples-title">
              <FaImages /> Choose a Sample Image
            </h4>
            <div className="samples-container">
              {sampleImages.map((sample) => (
                <motion.div
                  key={sample.id}
                  className="sample-card"
                  onClick={() => handleSampleSelect(sample)}
                  whileHover={{ scale: 1.05, y: -5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <div className="sample-image-wrapper">
                    <img
                      src={sample.path}
                      alt={sample.name}
                      onError={(e) => {
                        e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23667eea" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" fill="white" text-anchor="middle" dy=".3em" font-size="14"%3ENo Image%3C/text%3E%3C/svg%3E';
                      }}
                    />
                    <div className="sample-overlay">
                      <FaImage />
                      <span>Use This</span>
                    </div>
                  </div>
                  <div className="sample-info">
                    <h5>{sample.name}</h5>
                    <p>{sample.description}</p>
                    <span className="sample-category">{sample.category}</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default ImageUpload;
