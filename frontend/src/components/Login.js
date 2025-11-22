import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaUser, FaLock, FaRocket, FaUserPlus } from 'react-icons/fa';
import { toast } from 'react-toastify';
import './Login.css';

const Login = ({ onLogin }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // Get users from localStorage or use default admin
  const getUsers = () => {
    const users = localStorage.getItem('aiplatform_users');
    if (users) {
      return JSON.parse(users);
    }
    // Default admin user
    const defaultUsers = [{ username: 'admin', password: '12345' }];
    localStorage.setItem('aiplatform_users', JSON.stringify(defaultUsers));
    return defaultUsers;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isRegister) {
      // Registration logic
      if (!username || !password || !confirmPassword) {
        toast.error('Please fill all fields!');
        return;
      }
      
      if (password !== confirmPassword) {
        toast.error('Passwords do not match!');
        return;
      }
      
      if (password.length < 5) {
        toast.error('Password must be at least 5 characters!');
        return;
      }
      
      const users = getUsers();
      
      // Check if username already exists
      if (users.find(u => u.username === username)) {
        toast.error('Username already exists!');
        return;
      }
      
      // Add new user
      users.push({ username, password });
      localStorage.setItem('aiplatform_users', JSON.stringify(users));
      
      toast.success('✅ Registration successful! Please login.');
      setIsRegister(false);
      setUsername('');
      setPassword('');
      setConfirmPassword('');
    } else {
      // Login logic
      if (!username || !password) {
        toast.error('Please enter username and password!');
        return;
      }
      
      const users = getUsers();
      const user = users.find(u => u.username === username && u.password === password);
      
      if (user) {
        toast.success(`🎉 Welcome back, ${username}!`);
        localStorage.setItem('aiplatform_currentUser', username);
        onLogin(username);
      } else {
        toast.error('Invalid username or password!');
      }
    }
  };

  const toggleMode = () => {
    setIsRegister(!isRegister);
    setUsername('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="login-gradient-orb orb-1"></div>
        <div className="login-gradient-orb orb-2"></div>
        <div className="login-gradient-orb orb-3"></div>
      </div>

      <motion.div
        className="login-card"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="login-header">
          <div className="login-logo">
            <FaRocket className="login-logo-icon" />
          </div>
          <h1>AI Image Analysis Platform</h1>
          <p>{isRegister ? 'Create your account' : 'Welcome back!'}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <div className="input-icon">
              <FaUser />
            </div>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="login-input"
            />
          </div>

          <div className="input-group">
            <div className="input-icon">
              <FaLock />
            </div>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="login-input"
            />
          </div>

          {isRegister && (
            <motion.div
              className="input-group"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div className="input-icon">
                <FaLock />
              </div>
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="login-input"
              />
            </motion.div>
          )}

          <motion.button
            type="submit"
            className="login-button"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isRegister ? (
              <>
                <FaUserPlus /> Register
              </>
            ) : (
              <>
                <FaUser /> Login
              </>
            )}
          </motion.button>
        </form>

        <div className="login-footer">
          <p>
            {isRegister ? 'Already have an account?' : "Don't have an account?"}
            <button onClick={toggleMode} className="toggle-mode-btn">
              {isRegister ? 'Login' : 'Register'}
            </button>
          </p>
          
          {!isRegister && (
            <div className="default-credentials">
              <p className="hint-text">💡 Default credentials:</p>
              <p className="credentials">Username: <strong>admin</strong> | Password: <strong>12345</strong></p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default Login;
