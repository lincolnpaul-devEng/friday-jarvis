# Friday JARVIS - Render Deployment Ready ✅

This backend is fully prepared for **Docker-free deployment on Render.com**.

## 🚀 Quick Start

### Prerequisites
- GitHub account (with this repo pushed)
- Render.com account (free, no credit card needed)
- LiveKit credentials

### Deploy in 3 Steps

1. **Sign up on Render** → https://render.com → Click "Sign up with GitHub"
2. **Create Web Service**
   - Connect this GitHub repository
   - Render auto-detects `render.yaml`
   - Click "Create Web Service"
3. **Add Secrets**
   - Go to service settings → "Environment"
   - Add these variables:
     ```
     LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
     LIVEKIT_API_KEY=your-key
     LIVEKIT_API_SECRET=your-secret
     GOOGLE_API_KEY=your-api-key
     GMAIL_USER=your-email@gmail.com
     GMAIL_APP_PASSWORD=your-app-password
     ```

**Done!** Your agent will be live in 2-3 minutes.

---

## 📁 Backend Structure

```
friday-jarvis/
├── agent.py              # Main LiveKit agent entrypoint
├── tools.py              # Weather, web search, email functions
├── prompts.py            # Agent personality and instructions
├── requirements.txt      # Python dependencies
├── render.yaml          # ✅ Render deployment config (UPDATED)
├── .env.example         # ✅ Environment variable template (UPDATED)
└── README.md            # This file
```

### Removed Files ❌
- `Dockerfile` - Removed to avoid Docker conflicts
- `.dockerignore` - Removed to avoid Docker conflicts

These have been removed because Render's native Python 3.11 runtime is faster and simpler than Docker for this use case.

---

## 🔧 Configuration Files

### render.yaml
```yaml
services:
  - type: web
    name: friday-jarvis
    runtime: python
    pythonVersion: 3.11
    buildCommand: pip install -r requirements.txt
    startCommand: python -m livekit.agents agent
    plan: free
```

**What it does:**
- Tells Render to use Python 3.11
- Installs dependencies from `requirements.txt`
- Starts the agent with: `python -m livekit.agents agent`
- Uses free tier (750 compute hours/month)

### requirements.txt
All Python dependencies needed:
```
livekit-agents
livekit-plugins-openai
livekit-plugins-silero
livekit-plugins-google
livekit-plugins-noise-cancellation
mem0ai
duckduckgo-search
langchain_community
requests
python-dotenv
```

### .env.example
Template for environment variables (you fill in your actual values).

---

## 🛠️ Features Implemented

### Tools
- ✅ **get_weather** - Get current weather for any city
- ✅ **search_web** - Search the web using DuckDuckGo
- ✅ **send_email** - Send emails via Gmail with optional CC

### AI Model
- **Google Realtime LLM** - Real-time voice processing
- **Noise Cancellation** - Built-in BVC noise cancellation
- **Voice Output** - Aoede voice synthesis

### Infrastructure
- ✅ **LiveKit Cloud** - WebSocket-based voice sessions
- ✅ **Retry Logic** - 3-attempt auto-retry with exponential backoff
- ✅ **Logging** - Full DEBUG-level logging for troubleshooting

---

## 📝 Environment Variables Required

| Variable | Source | Required? |
|----------|--------|-----------|
| LIVEKIT_URL | LiveKit Dashboard | ✅ Yes |
| LIVEKIT_API_KEY | LiveKit Dashboard | ✅ Yes |
| LIVEKIT_API_SECRET | LiveKit Dashboard | ✅ Yes |
| GOOGLE_API_KEY | Google Cloud Console | ✅ Yes |
| GMAIL_USER | Your email | ✅ Yes |
| GMAIL_APP_PASSWORD | Gmail App Passwords | ✅ Yes |
| OPENROUTER_API_KEY | OpenRouter.ai | ⚠️ Optional |

---

## 🔐 Getting Credentials

### LiveKit
1. Go to https://cloud.livekit.io
2. Create an account or sign in
3. Create a new room or project
4. Copy URL, API Key, and Secret

### Google API Key
1. Go to https://console.cloud.google.com/apis/credentials
2. Create → API Key
3. Enable "Google Cloud Speech-to-Text" and "Google Generative AI"

### Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Generate and copy the 16-character password

---

## 🚢 Deployment Process

### Full Deployment (Recommended)
1. Push changes to GitHub
2. Render automatically detects `render.yaml`
3. Render builds and deploys in ~2 minutes
4. Service gets a unique URL

### Manual Deployment
1. Open https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Render finds `render.yaml` automatically
5. Click "Create Web Service"

---

## 📊 Render.com Pricing

| Plan | Cost | Compute Hours | Best For |
|------|------|---------------|----------|
| Free | $0 | 750/month | Development, light testing |
| Pro | $7 | Unlimited | Production, always-on |

### Cost Calculation
- **750 hours = 31 days of 24/7 usage**
- If you use 2 instances, you get 375 hours each (15 days 24/7)
- Most projects stay within free tier

---

## 🎯 Production Checklist

Before going live:

- [ ] All environment variables added to Render dashboard
- [ ] `render.yaml` is correct and pushed to GitHub
- [ ] `requirements.txt` has all dependencies
- [ ] Agent starts without errors (check Render Logs)
- [ ] Android app TokenExt.kt has correct Render URL
- [ ] Test with UptimeRobot to keep service warm (free tier)
- [ ] Monitor Render logs daily for errors
- [ ] Set up error alerting (optional but recommended)

---

## 🐛 Troubleshooting

### "Build failed" Error
Check `requirements.txt` for all dependencies. Render logs will show the exact missing package.

```powershell
# Test locally first
pip install -r requirements.txt
```

### Service won't start
```
Error: ModuleNotFoundError: No module named 'livekit'
```
The build didn't complete properly. In Render dashboard:
1. Click the service
2. Scroll to "Logs"
3. Click "Retry Deploy"

### Service goes to sleep (free tier)
After 15 minutes of inactivity, Render spins down the service.
- **Fix:** Use UptimeRobot to ping every 10 minutes
- Or upgrade to Pro ($7/month) for always-on

### Agent not responding
1. Check Render Logs for connection errors
2. Verify environment variables are set
3. Check that the Android app has the correct URL
4. Ensure LiveKit credentials are valid

---

## 📈 Performance Notes

- **Cold Start:** ~30 seconds on free tier (service wakes up)
- **Warm Start:** <1 second (service already running)
- **Response Time:** 2-5 seconds (LLM processing)
- **Concurrent Users (Free):** 1 device at a time

---

## 🔄 Auto-Deploy on Git Push

Render automatically redeploys when you push to GitHub:

```powershell
# Make changes to agent.py, tools.py, etc.
git add .
git commit -m "Update agent functionality"
git push origin main

# Render detects the push and redeploys in ~2 minutes
# Watch Render Logs to see the deployment
```

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs/python
- **LiveKit Docs:** https://docs.livekit.io
- **Python Agent Framework:** https://docs.livekit.io/agents/overview
- **Deployment Guide:** See `RENDER_DEPLOYMENT_GUIDE.md` for detailed walkthrough

---

## ✨ Why Docker-Free?

This deployment uses Render's native Python runtime instead of Docker because:

✅ **Faster:** No Docker image build overhead  
✅ **Simpler:** Fewer configuration layers  
✅ **Better logs:** Python output goes directly to Render logs  
✅ **Smaller:** No Docker daemon or container layer  
✅ **Cheaper:** Slightly lower resource overhead  

Docker would be overkill for a simple Python agent.

---

## 🎯 Next Steps

1. **Test Locally**
   ```powershell
   pip install -r requirements.txt
   python -m livekit.agents agent
   ```

2. **Push to GitHub**
   ```powershell
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

3. **Deploy to Render**
   - Sign up: https://render.com
   - Connect GitHub repo
   - Add environment variables
   - Done! 🚀

4. **Update Android App**
   - Get Render URL from dashboard
   - Update `TokenExt.kt` with the URL
   - Build and test

---

## 📞 Support

If you hit issues:
1. Check Render Logs (most informative)
2. Read `RENDER_DEPLOYMENT_GUIDE.md` (step-by-step)
3. Check `requirements.txt` for missing dependencies
4. Verify all environment variables are set

---

**Status:** ✅ Ready for Render Deployment

**Last Updated:** January 7, 2026

**Docker Status:** ❌ Removed (using native Python runtime)
