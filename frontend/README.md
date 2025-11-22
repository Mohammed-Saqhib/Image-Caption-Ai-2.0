# Image AI Frontend

Modern React frontend for AI-powered image analysis featuring OCR, captioning, translation, and text-to-speech.

## 🚀 Features

- **📸 Image Upload**: Drag-and-drop or click to upload
- **🔍 OCR**: Multi-language text extraction from images
- **🤖 AI Captioning**: Generate intelligent image descriptions
- **🌍 Translation**: Translate text into 19+ languages
- **🔊 Text-to-Speech**: Convert text to natural audio

## 🛠️ Tech Stack

- **React 18.2.0**: Modern UI framework
- **Framer Motion 10.16.0**: Smooth animations
- **Axios**: API communication
- **React Toastify**: Toast notifications
- **React Icons**: Beautiful icons
- **React Dropzone**: File upload handling

## 📦 Installation

```bash
cd frontend
npm install
```

## 🔧 Configuration

Create a `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
```

For production (Vercel):
- Set environment variable: `REACT_APP_API_URL` = `https://your-backend-url.hf.space`

## 🏃 Run Development

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000)

## 🏗️ Build for Production

```bash
npm run build
```

## 🌐 Deploy to Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_REPO_URL&project-name=image-ai-frontend&env=REACT_APP_API_URL)

### Manual Deploy

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

4. Set environment variable:
```bash
vercel env add REACT_APP_API_URL
# Enter: https://your-backend.hf.space
```

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Header.js/css
│   │   ├── ImageUpload.js/css
│   │   ├── TabNavigation.js/css
│   │   ├── OCRPanel.js/css
│   │   ├── CaptionPanel.js/css
│   │   ├── TranslationPanel.js/css
│   │   └── TTSPanel.js/css
│   ├── services/
│   │   └── api.js
│   ├── App.js/css
│   └── index.js/css
├── package.json
├── vercel.json
└── README.md
```

## 🎨 Components

### Header
- App branding and navigation
- Links to GitHub/docs

### ImageUpload
- Drag-and-drop file upload
- Image preview with metadata
- Remove/replace functionality

### TabNavigation
- Switch between features
- Icons and descriptions

### OCRPanel
- Multi-language selection
- Text extraction from images
- Copy/download results

### CaptionPanel
- AI image description
- Cloud/local mode selection
- Confidence scoring

### TranslationPanel
- Source text input
- Target language selection
- Side-by-side translation view

### TTSPanel
- Text-to-speech conversion
- Voice/language selection
- Speech rate control
- Audio playback/download

## 🔌 API Integration

All API calls are centralized in `src/services/api.js`:

```javascript
import * as api from './services/api';

// Upload image
await api.uploadImage(file);

// Extract text (OCR)
await api.performOCR(file, ['en', 'es']);

// Generate caption
await api.generateCaption(file, 'cloud');

// Translate text
await api.translateText(text, 'es');

// Text-to-speech
await api.textToSpeech(text, 'en', 200);
```

## 🎨 Styling

Custom CSS with:
- Modern gradient backgrounds
- Smooth animations via Framer Motion
- Responsive design (mobile-first)
- Custom scrollbar styling
- Toast notifications
- Loading states

## 🌍 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `https://username-app.hf.space` |

## 📱 Responsive Design

- **Desktop**: Full grid layout (1400px max-width)
- **Tablet**: Stacked layout (< 1024px)
- **Mobile**: Single column, optimized controls (< 768px)

## 🐛 Troubleshooting

### CORS Errors
Ensure backend has CORS configured:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Failed
1. Check `REACT_APP_API_URL` is set correctly
2. Verify backend is running
3. Check browser console for errors

### Build Fails
1. Clear node_modules: `rm -rf node_modules`
2. Reinstall: `npm install`
3. Rebuild: `npm run build`

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ using React + Vercel**
