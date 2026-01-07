# Render.com Deployment Guide - Friday JARVIS Backend
**Complete Step-by-Step (No Credit Card Required)**

⚠️ **IMPORTANT: Docker-Free Deployment**
This guide uses **pure Python deployment** on Render. Docker images have been removed to avoid conflicts with Render's native Python runtime.

---

## Why Render Over Others?

| Feature | Render | Railway | GCP Cloud Run | Heroku |
|---------|--------|---------|---------------|--------|
| Credit Card Required | ❌ No | ⚠️ Yes ($5/mo) | ⚠️ Yes | ❌ No (but dead) |
| Free Hours/Month | 750 hours | $5 credits | 2M requests | 0 (removed) |
| WebSocket Support | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Removed |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ Dead |
| GitHub Integration | ✅ Auto-deploy | ✅ Auto-deploy | ⚠️ Manual | ❌ |

---

## Prerequisites

1. **GitHub Account** - You already have `friday-jarvis` pushed here ✅
2. **Render Account** - Sign up at [render.com](https://render.com) (use GitHub OAuth = instant)
3. **Your LiveKit Credentials** - Have these ready:
   ```
   LIVEKIT_URL=wss://friday-uk2toy5r.livekit.cloud
   LIVEKIT_API_KEY=APIYnzgriSNVjbG
   LIVEKIT_API_SECRET=0nICJFFHqmYECGsZ31pUR3EE98KUxaUbPlfPC4IFirX
   ```

---

## STEP 1: Sign Up on Render (2 minutes)

### 1.1 Go to Render.com
- Open: https://render.com
- Click **"Get Started"** (top right)
- Click **"Sign up with GitHub"**
- Authorize Render to access your repositories

### 1.2 Verify Email
- Render sends a confirmation email
- Click the link
- Done! You're authenticated

---

## STEP 2: Configuration Files (Already Set Up) ✅

Your repo now has the correct configuration for Render **without Docker**:

### 2.1 render.yaml Configuration

**File:** `render.yaml`

```yaml
services:
  - type: web
    name: friday-jarvis
    runtime: python
    pythonVersion: 3.11
    buildCommand: pip install -r requirements.txt
    startCommand: python agent.py dev
    envVars:
      - key: PYTHONUNBUFFERED
        value: "1"
    plan: free
```

✅ **No Docker needed!** Render uses Python runtime directly. This command links to LiveKit Playground.

### 2.2 Dependencies Configuration

**File:** `requirements.txt`

All required packages are listed:
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

### 2.3 Environment Variables

**File:** `.env.example`

All required environment variables are documented. Render will use your `.env` secrets at runtime.

### 2.4 Removed Files ✅

The following Docker files have been **removed** to avoid deployment conflicts:
- ❌ `Dockerfile` (removed)
- ❌ `.dockerignore` (removed)

This ensures Render uses its native Python 3.11 runtime without Docker overhead.

---

## STEP 3: Create Render.yaml Config (5 minutes)

### 3.1 Go to Render Dashboard
- Open: https://dashboard.render.com
- Click **"New +"** (top right)
- Select **"Web Service"**

### 3.2 Connect GitHub Repository
- Click **"Connect account"** (if needed)
- Search for **"friday-jarvis"**
- Click **"Connect"** next to your repo

### 4.2 Configure Service

**Fill in these fields:**

| Field | Value |
|-------|-------|
| **Name** | friday-jarvis |
| **Root Directory** | (leave blank) |
| **Runtime** | Python 3.11 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python agent.py dev` |
| **Plan** | Free |

### 4.3 Environment Variables (Recommended: Use Dashboard)

### 4.3 Environment Variables (Recommended: Use Dashboard)

**Recommended approach:** Add secrets via Render dashboard (more secure than hardcoding):

```
LIVEKIT_URL=wss://friday-uk2toy5r.livekit.cloud
LIVEKIT_API_KEY=APIYnzgriSNVjbG
LIVEKIT_API_SECRET=0nICJFFHqmYECGsZ31pUR3EE98KUxaUbPlfPC4IFirX
GOOGLE_API_KEY=your_key_here
GMAIL_APP_PASSWORD=your_password_here
GMAIL_USER=your_email@gmail.com
OPENROUTER_API_KEY=your_key_here (optional)
```

Each value goes in a separate `Environment Variable` field in the Render dashboard.

### 4.4 Click **"Create Web Service"**

Render will:
1. Clone your GitHub repo
2. Install Python 3.11
3. Install dependencies from `requirements.txt`
4. Start with `python agent.py dev` (LiveKit Playground integration)
5. Assign a public URL like: `https://friday-jarvis-xxxx.onrender.com`

**Wait 2-3 minutes** for deployment to complete.

---

## STEP 5: Get Your Service URL (1 minute)

### 5.1 Find URL in Render Dashboard

Once deployment completes (green checkmark):
- Go to https://dashboard.render.com
- Click **"friday-jarvis"** service
- Look for **"Render URL"** at the top

Example:
```
https://friday-jarvis-abc123.onrender.com
```

### 5.2 Copy and Save This URL

You'll need it in the next step.

---

## STEP 6: Update Android App (5 minutes)

### 6.1 Edit TokenExt.kt

File: `Maya\app\src\main\java\io\livekit\android\example\voiceassistant\TokenExt.kt`

```kotlin
package io.livekit.android.example.voiceassistant

const val sandboxID = ""  // Keep empty - using custom backend

// Replace with YOUR Render URL from STEP 5
const val hardcodedUrl = "https://friday-jarvis-abc123.onrender.com"

// Leave empty for now - we'll test with the URL first
const val hardcodedToken = ""
```

### 6.2 Build APK

```powershell
cd C:\Users\paull\Desktop\friday_jarvis\Maya

./gradlew assembleRelease
```

APK appears at: `Maya\app\build\outputs\apk\release\app-release.apk`

### 6.3 Optional: Install on Device

```powershell
adb install Maya\app\build\outputs\apk\release\app-release.apk
```

---

## STEP 7: View Logs & Verify (2 minutes)

### 7.1 Open Render Logs

- In Render dashboard for "friday-jarvis" service
- Scroll to **"Logs"** section
- Should see:
  ```
  Starting Python agent...
  Agent initialized successfully
  Waiting for connections...
  ```

### 7.2 Test Connection from Android

1. Open Friday JARVIS app on device
2. Tap **"[ INITIALIZE CALL ]"**
3. Grant microphone permission
4. Say something to test

### 7.3 Watch Logs for Activity

In Render Logs, you should see:
```
Connection received from [device-ip]
Audio stream started
Processing with Google Realtime LLM...
Response: "Hello! How can I assist you?"
```

---

## STEP 8: Known Limitations & Solutions

### ⚠️ Free Plan Limitations

### ⚠️ Free Plan Limitations

| Limit | Value | Impact |
|-------|-------|--------|
| **Compute Hours/Month** | 750 | ~1 instance 24/7, or 2 instances 12 hours/day |
| **Idle Spin-down** | 15 min inactivity | Service sleeps, auto-wakes on request (~30s startup) |
| **Shared Resources** | CPU/RAM shared | Slower than paid, but fine for voice |
| **Max Connections** | 1 (free) | One device at a time (upgrade for multi-user) |

### Solution: Keep Service Warm (Optional)

If service spins down during testing:
```powershell
# Add this to a scheduled task or run in background
$url = "https://friday-jarvis-abc123.onrender.com"
while ($true) {
    curl $url | Out-Null
    Start-Sleep -Seconds 600  # Ping every 10 minutes
}
```

Or use a free service like [UptimeRobot](https://uptimerobot.com):
1. Create account
2. Add monitor: your Render URL
3. Set check interval to 10 minutes

---

## STEP 9: Upgrade Path (When Needed)

### Free → Paid (if you hit limits)

### When to upgrade:
- Multiple concurrent users
- More than 750 compute hours/month
- Want faster startup (no idle spin-down)

### Upgrade options:
```
Free Plan:     $0/month (750 hours)
Pro Plan:      $7/month (unlimited compute, no spin-down)
```

Click **"Plan"** in Render dashboard → **"Upgrade to Pro"** → Add credit card.

---

## STEP 10: Troubleshooting

### Issue: "Build failed"
```
In Render Logs, look for error like:
  ERROR: Could not find a version that satisfies the requirement...
```
**Fix:** Check `requirements.txt` has all dependencies:
```
livekit-agents
livekit-plugins-google
...
```

### Issue: "Service won't start"
```
Error: ModuleNotFoundError: No module named 'livekit'
```
**Fix:** Render didn't install dependencies. Restart:
- In Render dashboard, click **"Logs"**
- Click **"Retry Deploy"** button

### Issue: "Android app connects but no response"
```
Check:
1. Render URL is correct in TokenExt.kt
2. Service shows "Running" (green) in dashboard
3. Check Render Logs for connection attempts
```

### Issue: Service keeps spinning down (free tier)
```
Solution:
- Use UptimeRobot to ping every 10 minutes
- Or upgrade to Pro ($7/month)
- Or restructure as scheduled job (different approach)
```

---

## STEP 11: Monitor & Maintain

### Weekly Checks
- [ ] Open Render dashboard → Check service status
- [ ] Click **"Logs"** → Verify no errors
- [ ] Test app once → Confirm still connecting

### Monthly
- [ ] Check compute hours used (Dashboard → Metrics)
- [ ] Review error logs for patterns
- [ ] Update agent code if needed → Git push auto-redeploys

---

## Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| **Render Hosting** | $0/month | 750 free hours = ~31 days of 24/7 runtime |
| **GitHub** | $0/month | Free public repo |
| **LiveKit Cloud** | $0/month | Using your existing account |
| **Total** | **$0/month** | Completely free! |

---

## Quick Reference Commands

```powershell
# Push code to deploy
git add .
git commit -m "Update code"
git push origin main

# View live logs
# (Open in browser: https://dashboard.render.com → friday-jarvis → Logs)

# Restart service if stuck
# (In dashboard: click the "..." menu → Restart)

# Get service URL
# (In dashboard: Copy from "Render URL" field)
```

---

## Next Steps After Deployment

1. **Test with multiple devices** (if upgraded to paid)
2. **Monitor logs daily** for first week
3. **Optimize agent** based on real usage
4. **Add error alerting** (optional)
5. **Plan scaling** as user base grows

---

## Comparison: Render vs GCP

| Aspect | Render | GCP |
|--------|--------|-----|
| **Setup Time** | 10 minutes | 30 minutes |
| **Credit Card** | ❌ Not needed | ✅ Required |
| **Free Cost** | $0/month | $0/month (first tier) |
| **Complexity** | Simple YAML | Complex gcloud CLI |
| **Python WebSocket** | ✅ Perfect | ✅ Good |
| **Scaling** | Easy (pay more) | Complex (APIs) |

**For you: Render is the obvious choice** ✅

---

## STEP 12: Estimated Timeline

- **STEP 1** (Sign up): 2 min
- **STEP 2** (Configuration check): 1 min
- **STEP 3** (Deploy service): 5 min
- **STEP 4** (Build/deployment): 2 min
- **STEP 5** (Get URL): 1 min
- **STEP 6** (Update Android): 5 min
- **STEP 7** (Verify): 2 min

**Total: ~18 minutes to production** 🚀

---

## Key Advantages of This Docker-Free Setup

✅ **Faster deployment** - No Docker build overhead  
✅ **Smaller footprint** - Native Python runtime only  
✅ **Better cold starts** - Render Python runtime is optimized  
✅ **Easier debugging** - Render logs show Python output directly  
✅ **Fewer conflicts** - No Docker version issues  

---

## Next Steps After Deployment

1. **Test with multiple devices** (if upgraded to paid)
2. **Monitor logs daily** for first week
3. **Optimize agent** based on real usage
4. **Add error alerting** (optional)
5. **Plan scaling** as user base grows

---

**Ready? Let's deploy!** 🚀
