# ⚙️ Vercel Environment Variable Setup

## Problem
The OCR and other API features are not working on the deployed Vercel site because the backend API URL environment variable is not configured in Vercel.

## Solution

### Step 1: Go to Vercel Dashboard
1. Visit [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project: **image-ai-frontend** or similar

### Step 2: Add Environment Variable
1. Click on **Settings** tab
2. Click on **Environment Variables** in the left sidebar
3. Add the following environment variable:

```
Name: REACT_APP_API_URL
Value: https://saqhib-ai-image-analysis-backend.hf.space
Environment: Production, Preview, Development (select all)
```

### Step 3: Redeploy
1. Go to **Deployments** tab
2. Click on the three dots (...) next to the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete

## Verification

After redeployment, test the following:
- ✅ Sample images should load
- ✅ OCR text extraction should work
- ✅ AI caption generation should work
- ✅ Translation should work
- ✅ Text-to-Speech should work

## Alternative: Using Vercel CLI

You can also set the environment variable using Vercel CLI:

```bash
vercel env add REACT_APP_API_URL
# When prompted, enter: https://saqhib-ai-image-analysis-backend.hf.space
# Select: Production, Preview, Development
```

Then redeploy:
```bash
vercel --prod
```

## Important Notes

1. **Environment variables MUST start with `REACT_APP_`** for Create React App to recognize them
2. Changes to environment variables require a **full redeployment** (not just a rebuild)
3. The backend URL should be: `https://saqhib-ai-image-analysis-backend.hf.space`
4. No trailing slash in the URL

## Troubleshooting

If the API still doesn't work after setting the environment variable:

1. **Check browser console** for any CORS or network errors
2. **Verify backend is running**: Visit https://saqhib-ai-image-analysis-backend.hf.space/api/health
3. **Check Network tab** in browser DevTools to see the actual API URL being called
4. **Clear Vercel build cache**: Go to Settings → General → Clear Build Cache

## Current Status

- ✅ Sample images: **FIXED** (routing configured in vercel.json)
- ⚠️ OCR/API features: **NEEDS ENV VARIABLE** (follow steps above)

## Backend API Endpoints

All endpoints are working and can be tested:

- Health: `GET /api/health`
- OCR: `POST /api/ocr`
- Caption: `POST /api/caption`
- Translate: `POST /api/translate`
- TTS: `POST /api/tts`

Test backend health:
```bash
curl https://saqhib-ai-image-analysis-backend.hf.space/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "engines": {
    "ocr": "ready",
    "caption": "ready",
    "translation": "ready",
    "tts": "ready"
  }
}
```
