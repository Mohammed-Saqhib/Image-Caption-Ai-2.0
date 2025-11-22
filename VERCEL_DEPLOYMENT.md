# 🚀 Vercel Frontend Deployment Guide

## Your Hugging Face Backend URL
```
https://saqhib-ai-image-analysis-backend.hf.space
```

## Quick Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Login with your account

2. **Connect GitHub Repository**
   - Click "Add New..." → "Project"
   - Import your GitHub repository: `Mohammed-Saqhib/Image-Caption-Ai-2.0`
   - Select the repository

3. **Configure Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add this variable:
     ```
     Name: REACT_APP_API_URL
     Value: https://saqhib-ai-image-analysis-backend.hf.space
     ```
   - Select: Production, Preview, Development (all three)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment to complete
   - Your app will be live!

---

### Option 2: Deploy via CLI

1. **In your terminal, run:**
   ```bash
   cd /Users/sabaanjum/Desktop/Image\ Ai\ Work\ 1/frontend
   npx vercel
   ```

2. **Follow the prompts:**
   - Set up and deploy? **Yes**
   - Which scope? Select your account
   - Link to existing project? **No**
   - What's your project's name? **ai-image-analysis-frontend**
   - In which directory is your code located? **./frontend** or just press Enter
   - Want to modify settings? **Yes**
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Development Command: `npm start`

3. **Add Environment Variable (after first deployment):**
   ```bash
   npx vercel env add REACT_APP_API_URL
   ```
   - Enter the value: `https://saqhib-ai-image-analysis-backend.hf.space`
   - Select: Production, Preview, Development

4. **Redeploy with environment variable:**
   ```bash
   npx vercel --prod
   ```

---

## Testing Your Deployment

Once deployed, your Vercel URL will look like:
```
https://ai-image-analysis-frontend.vercel.app
```

### Test All Features:

1. **Health Check**
   - Open browser console (F12)
   - Check if API calls go to Hugging Face backend

2. **Upload Image**
   - Upload a test image
   - Verify it connects to Hugging Face backend

3. **Test OCR**
   - Upload image with text
   - Extract text

4. **Test AI Caption**
   - Upload any image
   - Generate caption

5. **Test Translation**
   - Translate extracted text or caption
   - Try different languages

6. **Test Text-to-Speech**
   - Convert text to speech
   - Download and play audio file

---

## Troubleshooting

### CORS Errors
If you see CORS errors in browser console:
- ✅ Already configured in backend (`allow_origins=["*"]`)
- The backend should accept requests from any domain

### Environment Variable Not Working
If frontend still connects to localhost:
1. Check Vercel dashboard → Your Project → Settings → Environment Variables
2. Ensure `REACT_APP_API_URL` is set correctly
3. Redeploy the project after adding the variable

### Build Errors
If build fails:
- Check the build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`

---

## Your URLs

**Frontend (Vercel):** 
- Will be provided after deployment
- Usually: `https://your-project-name.vercel.app`

**Backend (Hugging Face):**
- `https://saqhib-ai-image-analysis-backend.hf.space`
- API Docs: `https://saqhib-ai-image-analysis-backend.hf.space/api/docs`

---

## Next Steps After Deployment

1. ✅ Test all features on the live site
2. ✅ Share the URL with users
3. ✅ Monitor Hugging Face Space logs for any backend issues
4. ✅ Check Vercel deployment logs for frontend issues

---

## Quick Commands Reference

```bash
# Login to Vercel
npx vercel login

# Deploy to preview
npx vercel

# Deploy to production
npx vercel --prod

# View deployment logs
npx vercel logs

# List projects
npx vercel ls

# Add environment variable
npx vercel env add REACT_APP_API_URL
```

---

## Support

If you encounter any issues:
- Check Vercel logs: `npx vercel logs`
- Check Hugging Face Space logs: Click "Logs" tab on Space page
- Verify API calls in browser DevTools → Network tab

**Your deployment is ready! 🎉**
