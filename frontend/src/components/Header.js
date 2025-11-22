import React from 'react';
import { motion } from 'framer-motion';
import { FaRocket, FaGithub, FaLinkedin } from 'react-icons/fa';
import './Header.css';

const Header = () => {
  return (
    <motion.header
      className="header"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', stiffness: 100 }}
    >
      <div className="header-content">
        <div className="logo">
          <FaRocket className="logo-icon" />
          <h1>AI Image Analysis Platform</h1>
        </div>
        
        <div className="header-links">
          <a
            href="https://github.com/Mohammed-Saqhib/Image-Caption-Ai-2.0"
            target="_blank"
            rel="noopener noreferrer"
            className="header-link"
          >
            <FaGithub /> GitHub
          </a>
          <a
            href="https://linkedin.com"
            target="_blank"
            rel="noopener noreferrer"
            className="header-link"
          >
            <FaLinkedin /> LinkedIn
          </a>
        </div>
      </div>
      
      <div className="header-subtitle">
        <span className="badge">OCR</span>
        <span className="badge">AI Captioning</span>
        <span className="badge">Translation</span>
        <span className="badge">Text-to-Speech</span>
      </div>
    </motion.header>
  );
};

export default Header;
