import React from 'react';
import { motion } from 'framer-motion';
import { FaEye, FaImage, FaLanguage, FaVolumeUp } from 'react-icons/fa';
import './TabNavigation.css';

const tabs = [
  { id: 'ocr', name: 'OCR', icon: FaEye, desc: 'Extract Text' },
  { id: 'caption', name: 'AI Caption', icon: FaImage, desc: 'Generate Description' },
  { id: 'translation', name: 'Translate', icon: FaLanguage, desc: 'Multi-Language' },
  { id: 'tts', name: 'Speech', icon: FaVolumeUp, desc: 'Text-to-Speech' }
];

const TabNavigation = ({ activeTab, setActiveTab }) => {
  return (
    <div className="tab-navigation">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        return (
          <motion.button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Icon className="tab-icon" />
            <div className="tab-content">
              <span className="tab-name">{tab.name}</span>
              <span className="tab-desc">{tab.desc}</span>
            </div>
            {activeTab === tab.id && (
              <motion.div
                className="tab-indicator"
                layoutId="activeTab"
                initial={false}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
            )}
          </motion.button>
        );
      })}
    </div>
  );
};

export default TabNavigation;
