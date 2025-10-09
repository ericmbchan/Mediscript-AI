# 🚀 Render Deployment Guide for Mediscript Backend

This guide will walk you through deploying your Flask medical documentation API to Render.com - completely free!

## 📋 Prerequisites

- ✅ Your Flask application code (already ready!)
- ✅ GitHub account
- ✅ OpenAI API key
- ✅ 10 minutes of time

## 🛠️ Step 1: Prepare Your Code

### 1.1 Check Your Files
Your project should have these files in the `backend` directory:
```
backend/
├── Procfile              ✅ (created)
├── requirements.txt      ✅ (already exists)
├── wsgi.py              ✅ (already exists)
├── app/
│   ├── __init__.py      ✅ (already exists)
│   ├── config.py        ✅ (already exists)
│   └── routes.py        ✅ (already exists)
└── .env                 ⚠️ (you'll create this locally)
```

### 1.2 Create .env File (for local testing)
Create a `.env` file in your backend directory:
```env
SECRET_KEY=your-very-secure-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key-here
FLASK_ENV=production
FLASK_DEBUG=0
```

## 📤 Step 2: Push to GitHub

### 2.1 Initialize Git Repository (if not already done)
```bash
# Navigate to your project root
cd "C:\Users\ericm\Desktop\FALL2025 STARTUP\Mediscript"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit - Mediscript Flask API"
```

### 2.2 Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name it: `mediscript-backend` (or any name you prefer)
4. Make it **Public** (required for free Render deployment)
5. **Don't** initialize with README (you already have files)
6. Click "Create repository"

### 2.3 Push to GitHub
```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/mediscript-backend.git

# Push your code
git push -u origin main
```

## 🌐 Step 3: Deploy to Render

### 3.1 Sign Up for Render
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your **GitHub account** (this connects your repositories)

### 3.2 Create New Web Service
1. In your Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Find your `mediscript-backend` repository
   - Click **"Connect"**

### 3.3 Configure Your Service
Fill in the following details:

**Basic Settings:**
- **Name**: `mediscript-backend` (or any name you like)
- **Environment**: `Python 3`
- **Region**: Choose closest to you (e.g., Oregon for US West)
- **Branch**: `main` (or `master` if you used that)

**Build & Deploy Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app` (or leave blank - Render will use Procfile)

### 3.4 Add Environment Variables
Click **"Add Environment Variable"** and add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `your-very-secure-secret-key-here` |
| `OPENAI_API_KEY` | `sk-your-openai-api-key-here` |
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `0` |

### 3.5 Deploy!
1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your Flask app with Gunicorn
   - Give you a live URL

## ✅ Step 4: Test Your Deployment

### 4.1 Check Deployment Status
- Your app will be available at: `https://your-app-name.onrender.com`
- First deployment takes 5-10 minutes
- You can watch the build logs in real-time

### 4.2 Test API Endpoints

#### Health Check
```bash
curl https://your-app-name.onrender.com/api/health
```
Expected response:
```json
{"status": "ok"}
```

#### Generate Medical Documentation
```bash
curl -X POST https://your-app-name.onrender.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Patient complains of chest pain and shortness of breath"}'
```

### 4.3 Test in Browser
- Visit: `https://your-app-name.onrender.com`
- You should see your frontend (if you have one) or API documentation

## 🔄 Step 5: Automatic Deployments

### 5.1 How It Works
- Every time you push to your GitHub repository
- Render automatically detects changes
- Rebuilds and redeploys your app
- Usually takes 2-5 minutes

### 5.2 Making Updates
```bash
# Make your changes to the code
# Then commit and push:
git add .
git commit -m "Updated medical documentation feature"
git push origin main
# Render will automatically deploy the update!
```

## 🆓 Render Free Tier Features

### What You Get for Free:
- ✅ **750 hours/month** (enough for 24/7 if you're the only user)
- ✅ **512MB RAM** (plenty for Flask apps)
- ✅ **Custom domain** support
- ✅ **Automatic SSL** (HTTPS)
- ✅ **Automatic deployments**
- ✅ **Build logs** and monitoring

### Limitations:
- ⚠️ **App sleeps** after 15 minutes of inactivity
- ⚠️ **Wake-up time**: ~30 seconds for first request after sleep
- ⚠️ **No persistent storage** (use external databases if needed)

## 🔧 Troubleshooting

### Common Issues:

#### 1. Build Fails
**Check build logs in Render dashboard:**
- Usually missing dependencies in `requirements.txt`
- Check Python version compatibility

#### 2. App Crashes on Start
**Check environment variables:**
- Make sure `OPENAI_API_KEY` is set correctly
- Verify `SECRET_KEY` is set

#### 3. API Returns 500 Errors
**Check application logs:**
- Look for OpenAI API key issues
- Check if all required environment variables are set

#### 4. App Takes Too Long to Start
**Normal for free tier:**
- First request after sleep takes ~30 seconds
- This is expected behavior on free tier

### Getting Help:
- Check Render's documentation: https://render.com/docs
- View logs in your Render dashboard
- Test your app locally first

## 🎉 Congratulations!

Your Flask medical documentation API is now live on the internet! 

### Your App Details:
- **URL**: `https://your-app-name.onrender.com`
- **API Health**: `https://your-app-name.onrender.com/api/health`
- **API Generate**: `https://your-app-name.onrender.com/api/generate`

### Next Steps:
1. **Share your API** with others
2. **Monitor usage** in Render dashboard
3. **Add features** and push updates
4. **Consider upgrading** if you need more resources

---

**Need help?** Check the Render documentation or test your app locally first to ensure everything works!
