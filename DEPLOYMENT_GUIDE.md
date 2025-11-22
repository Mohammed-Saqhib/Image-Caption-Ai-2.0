
# 🚀 Complete Deployment Guide

This guide will help you deploy your Image AI application with **frontend on Vercel** and **backend on Hugging Face Spaces** - completely free!

## � Prerequisites

- GitHub account
- Vercel account (free)
- Hugging Face account (free)
- Git installed locally

---

## 🎯 Deployment Strategy

| Component | Platform | Cost | Resources |
|-----------|----------|------|-----------|
| Frontend | Vercel | $0/month | Global CDN, Auto HTTPS |
| Backend | Hugging Face Spaces | $0/month | 16GB RAM, Free GPU |

---

## �️ Part 1: Deploy Backend to Hugging Face Spaces

### Step 1: Create a Hugging Face Space

1. Go to [Hugging Face](https://huggingface.co/)
2. Click on your profile → **New Space**
3. Configure:
   - **Name**: `image-ai-backend` (or any name you like)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU Basic (free) or upgrade to T4 GPU if needed
   - **Visibility**: Public or Private

### Step 2: Push Backend Code to Hugging Face

```bash
# Navigate to your project
cd "/Users/sabaanjum/Desktop/Image Ai Work 1"

# Add Hugging Face remote (replace USERNAME and SPACE-NAME)
cd backend
git init
git add .
git commit -m "Initial backend deployment"
git remote add space https://huggingface.co/spaces/USERNAME/SPACE-NAME
git push --force space main
```

### Step 3: Configure Environment (Optional)

If you use Hugging Face API for captioning:

1. Go to your Space settings
2. Add **Repository Secret**:
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face token (from Settings → Access Tokens)

### Step 4: Wait for Build

- Build time: 5-10 minutes
- Monitor logs in the Space's "Logs" tab
- Once complete, your API will be at: `https://USERNAME-SPACE-NAME.hf.space`

### Step 5: Test Backend API

```bash
# Test health endpoint
curl https://USERNAME-SPACE-NAME.hf.space/api/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}
```

---

## � Part 2: Deploy Frontend to Vercel

### Step 1: Push Frontend to GitHub

```bash
# Navigate to frontend directory
cd "/Users/sabaanjum/Desktop/Image Ai Work 1/frontend"

# Initialize git (if not already)
git init
git add .
git commit -m "Initial frontend deployment"

# Create GitHub repo and push
# Go to GitHub → New Repository → Create
git remote add origin https://github.com/YOUR-USERNAME/image-ai-frontend.git
git branch -M main
git push -u origin main
```

### Step 2: Import to Vercel

1. Go to [Vercel](https://vercel.com/)
2. Click **"Add New Project"**
3. Import your GitHub repository: `image-ai-frontend`
4. Configure build settings:
   - **Framework Preset**: Create React App
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

### Step 3: Add Environment Variable

1. In Vercel project settings → **Environment Variables**
2. Add variable:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://USERNAME-SPACE-NAME.hf.space` (your HF Space URL)
   - **Environments**: Production, Preview, Development

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Your app will be live at: `https://your-project.vercel.app`

### Step 5: Custom Domain (Optional)

1. Go to project **Settings → Domains**
2. Add your custom domain
3. Update DNS records as instructed

---

## 🔧 Part 3: Backend CORS Configuration

### Update Backend to Allow Vercel Frontend

Edit `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

# Add your Vercel URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-project.vercel.app",  # Your Vercel URL
        "https://your-custom-domain.com"  # If you have custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push to Hugging Face:

```bash
cd backend
git add main.py
git commit -m "Update CORS for Vercel frontend"
git push space main
```

---

## ✅ Part 4: Verification

### Test Complete Flow

1. **Open Frontend**: Go to `https://your-project.vercel.app`
2. **Upload Image**: Drag and drop an image
3. **Test OCR**: Select languages and extract text
4. **Test Caption**: Generate AI description
5. **Test Translation**: Translate extracted text
6. **Test TTS**: Convert text to speech

### Check API Connection

Open browser console (F12):
- Should see successful API calls
- No CORS errors
- Responses from Hugging Face backend

---

## 🐛 Troubleshooting

### Issue 1: CORS Error

**Symptom**: "Access to fetch has been blocked by CORS policy"

**Solution**:
1. Verify `REACT_APP_API_URL` in Vercel environment variables
2. Check backend CORS configuration includes Vercel URL
3. Redeploy backend after CORS changes

### Issue 2: API URL Not Working

**Symptom**: "Network Error" or "Failed to fetch"

**Solution**:
1. Check environment variable name is exactly: `REACT_APP_API_URL`
2. URL should NOT end with `/` (wrong: `https://....hf.space/`)
3. Redeploy Vercel after changing environment variables

### Issue 3: Backend Build Failed

**Symptom**: Hugging Face Space shows build error

**Solution**:
1. Check `backend/Dockerfile` is present
2. Verify `backend/requirements.txt` has all dependencies
3. Check Space logs for specific error
4. Try switching to CPU Basic hardware

### Issue 4: Images Not Loading in Production

**Symptom**: Upload works locally but not on Vercel

**Solution**:
1. Check file size limit (Vercel: 4.5MB for free tier)
2. Verify backend accepts multipart/form-data
3. Check browser console for errors

---

## � Continuous Deployment

### Auto-Deploy on Git Push

**Frontend (Vercel)**:
- Automatically deploys on every push to `main` branch
- Preview deployments for pull requests

**Backend (Hugging Face)**:
- Automatically rebuilds on every push to Space
- Check build status in Space logs

### Manual Redeploy

**Vercel**:
```bash
cd frontend
vercel --prod
```

**Hugging Face**:
```bash
cd backend
git push space main
```

---

## � Monitoring & Analytics

### Vercel Analytics (Free)

1. Go to project dashboard
2. Enable **Analytics** tab
3. View:
   - Page views
   - Top pages
   - User locations
   - Performance metrics

### Hugging Face Space Logs

1. Go to your Space
2. Click **Logs** tab
3. Monitor:
   - API requests
   - Errors
   - Performance

---

## 💰 Cost Breakdown

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| Vercel | Hobby | $0 | 100GB bandwidth/month |
| Hugging Face Spaces | Free | $0 | 16GB RAM, 50GB storage |
| **Total** | - | **$0/month** | Perfect for personal/portfolio projects |

---

## 🎓 Upgrade Options (If Needed)

### Vercel Pro ($20/month)
- Unlimited bandwidth
- Team collaboration
- Advanced analytics
- Password protection

### Hugging Face GPU ($0.60/hour)
- T4 GPU for faster AI inference
- Better for high traffic
- Pay-as-you-go

---

## 📚 Useful Commands

### Frontend Development
```bash
cd frontend
npm start              # Run locally
npm run build          # Build for production
npm test               # Run tests
vercel                 # Deploy to preview
vercel --prod          # Deploy to production
```

### Backend Development
```bash
cd backend
uvicorn main:app --reload  # Run locally
docker build -t app .      # Build Docker image
docker run -p 7860:7860 app # Test Docker locally
```

### Git Operations
```bash
# Update frontend
cd frontend
git add .
git commit -m "Update message"
git push origin main

# Update backend
cd backend
git add .
git commit -m "Update message"
git push space main
```

---

## 🎉 Success Checklist

- [ ] Backend deployed to Hugging Face Spaces
- [ ] Backend health endpoint returns 200 OK
- [ ] Frontend pushed to GitHub
- [ ] Frontend deployed to Vercel
- [ ] `REACT_APP_API_URL` environment variable set
- [ ] Backend CORS includes Vercel URL
- [ ] Image upload works in production
- [ ] OCR extraction works
- [ ] AI captioning works
- [ ] Translation works
- [ ] Text-to-speech works
- [ ] No console errors in browser

---

## 🆘 Getting Help

### Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)

### Support
- Create GitHub issue
- Vercel support (for Pro users)
- Hugging Face community forums

---

## 🎯 Next Steps

1. **Custom Domain**: Add your own domain to Vercel
2. **Analytics**: Enable Vercel Analytics for insights
3. **Monitoring**: Set up error tracking (Sentry)
4. **SEO**: Add meta tags for better discoverability
5. **PWA**: Make it installable as Progressive Web App
6. **Performance**: Optimize images and code splitting

---

**Happy Deploying! 🚀**

Your app is now live and accessible worldwide for free!
