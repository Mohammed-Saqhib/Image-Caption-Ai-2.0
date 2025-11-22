import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { FaCloudUploadAlt, FaImage } from 'react-icons/fa';
import './ImageUpload.css';

const ImageUpload = ({ onUpload, imagePreview, loading }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
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

  return (
    <motion.div
      className="image-upload-container"
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${loading ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />
        
        {imagePreview ? (
          <div className="image-preview">
            <img src={imagePreview} alt="Uploaded" />
            <div className="image-overlay">
              <FaImage size={30} />
              <p>Click or drag to change image</p>
            </div>
          </div>
        ) : (
          <div className="upload-prompt">
            <FaCloudUploadAlt size={60} className="upload-icon" />
            <h3>Drag & Drop Image Here</h3>
            <p>or click to browse</p>
            <span className="file-types">PNG, JPG, JPEG, GIF, WEBP (Max: 10MB)</span>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ImageUpload;
