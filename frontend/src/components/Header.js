import React from 'react';
import { motion } from 'framer-motion';
import { FaRocket, FaSignOutAlt, FaUser } from 'react-icons/fa';
import './Header.css';

const Header = ({ user, onLogout }) => {
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
        
        {user && (
          <div className="user-section">
            <div className="user-info">
              <FaUser className="user-icon" />
              <span className="username">{user}</span>
            </div>
            <motion.button
              className="logout-btn"
              onClick={onLogout}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaSignOutAlt /> Logout
            </motion.button>
          </div>
        )}
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
