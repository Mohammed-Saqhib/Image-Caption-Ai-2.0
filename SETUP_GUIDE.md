# 🚀 Quick Setup Guide - Install Required Tools

## Current Status:
- ✅ Python3 installed (`/usr/bin/python3`)
- ✅ Homebrew installed (`/opt/homebrew/bin/brew`)
- ❌ Node.js and npm NOT installed (needed for frontend)

---

## 📦 Step 1: Install Node.js and npm

### Using Homebrew (RECOMMENDED - Fast):

```bash
# Install Node.js (includes npm)
brew install node

# Verify installation
node --version
npm --version
```

**Time: 2-3 minutes**

---

## 🐍 Step 2: Setup Python Backend

```bash
# Navigate to backend
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/backend"

# Install dependencies
python3 -m pip install -r requirements.txt

# Run backend server
python3 -m uvicorn main:app --reload --port 8000
```

Backend will run at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

## ⚛️ Step 3: Setup React Frontend

```bash
# Navigate to frontend (in a NEW terminal)
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/frontend"

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Run frontend
npm start
```

Frontend will open at: **http://localhost:3000**

---

## 🎯 Quick Commands Summary

### Install Everything:
```bash
# 1. Install Node.js
brew install node

# 2. Install Python packages (backend)
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/backend"
python3 -m pip install -r requirements.txt

# 3. Install npm packages (frontend)
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/frontend"
npm install
```

### Run the Application:

**Terminal 1 - Backend:**
```bash
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/backend"
python3 -m uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/frontend"
npm start
```

---

## 🔧 Troubleshooting

### Issue: "zsh: command not found: npm"
**Solution**: Node.js not installed. Run `brew install node`

### Issue: "zsh: command not found: pip"
**Solution**: Use `python3 -m pip` instead of just `pip`

### Issue: "zsh: command not found: uvicorn"
**Solution**: Use `python3 -m uvicorn` instead of just `uvicorn`

### Issue: Port already in use
**Solution**: 
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python3 -m uvicorn main:app --reload --port 8001
```

---

## ✅ Verification

After installation, verify everything works:

```bash
# Check Node.js
node --version
# Should show: v20.x.x or similar

# Check npm
npm --version  
# Should show: 10.x.x or similar

# Check Python
python3 --version
# Should show: Python 3.x.x

# Check pip
python3 -m pip --version
# Should show: pip 24.x.x or similar
```

---

## 🎉 Next Steps

Once everything is installed and running:

1. ✅ Open http://localhost:3000 (Frontend)
2. ✅ Upload an image
3. ✅ Test OCR, Captioning, Translation, TTS
4. ✅ Check http://localhost:8000/docs (API Documentation)

Then proceed to **DEPLOYMENT_GUIDE.md** for deploying to production!

---

**Need Help?** Check the terminal output for specific error messages.
