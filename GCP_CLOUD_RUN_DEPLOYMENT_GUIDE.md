# Google Cloud Run Deployment Guide - Friday JARVIS Backend
**Complete Step-by-Step Instructions**

---

## Prerequisites (Before Starting)

1. **Google Account** - Create one at [google.com](https://google.com) if needed
2. **Google Cloud SDK** - Download from [cloud.google.com/sdk](https://cloud.google.com/sdk)
3. **Docker** - Install from [docker.com](https://docker.com) (or just use gcloud)
4. **Git** - Already have this (your code is in GitHub)
5. **Your LiveKit credentials** ready

---

## STEP 1: Create Google Cloud Project

### 1.1 Go to Google Cloud Console
- Open: https://console.cloud.google.com/
- Click "Select a Project" (top left)
- Click "New Project"

### 1.2 Create New Project
```
Project name: friday-jarvis
Location: No organization (or select your org)
```
- Click "Create"
- Wait ~30 seconds for project creation

### 1.3 Enable Cloud Run API
```
1. In console, search for "Cloud Run"
2. Click on "Cloud Run" service
3. Click "Enable" (blue button)
4. Wait for API to enable (~1 minute)
```

### 1.4 Enable Artifact Registry API
```
1. Search for "Artifact Registry"
2. Click "Enable"
3. Wait for API to enable
```

### 1.5 Enable Container Registry API (for image storage)
```
1. Search for "Container Registry"
2. Click "Enable"
```

---

## STEP 2: Set Up Google Cloud SDK

### 2.1 Install Google Cloud SDK
**Windows:**
- Download: https://cloud.google.com/sdk/docs/install#windows
- Run installer
- In terminal, verify installation:
```powershell
gcloud --version
```

### 2.2 Authenticate with Google Cloud
```powershell
gcloud auth login
```
- Browser opens
- Click your Google account
- Click "Allow" to grant permissions
- Return to terminal (should say "You are now authenticated")

### 2.3 Set Your Project
```powershell
gcloud config set project friday-jarvis
```
Replace `friday-jarvis` with your actual project name if different.

### 2.4 Verify Setup
```powershell
gcloud config list
```
Should show:
```
[core]
account = your.email@gmail.com
project = friday-jarvis
```

---

## STEP 3: Prepare Code for Cloud Run

### 3.1 Create Dockerfile
In your project root (`c:\Users\paull\Desktop\friday_jarvis\`), create file: `Dockerfile`

```dockerfile
# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent.py .
COPY tools.py .
COPY prompts.py .

# Set environment variables (will be overridden by Cloud Run)
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run the agent
CMD ["python", "-m", "livekit.agents", "agent"]
```

### 3.2 Create .dockerignore
In project root, create `.dockerignore`:
```
__pycache__
.git
.env
*.pyc
.pytest_cache
.venv
venv
Maya
KMS
```

### 3.3 Verify requirements.txt
Check that `requirements.txt` exists with all dependencies:
```
livekit-agents
livekit-plugins-openai
livekit-plugins-silero
livekit-plugins-google
livekit-plugins-noise-cancellation
duckduckgo-search
langchain_community
requests
python-dotenv
```

### 3.4 Create .env.example
In project root, create `.env.example` (for reference):
```
LIVEKIT_URL=wss://friday-uk2toy5r.livekit.cloud
LIVEKIT_API_KEY=APIYnzgriSNVjbG
LIVEKIT_API_SECRET=0nICJFFHqmYECGsZ31pUR3EE98KUxaUbPlfPC4IFirX
GOOGLE_API_KEY=your_google_api_key_here
GMAIL_APP_PASSWORD=your_gmail_app_password
GMAIL_USER=your_email@gmail.com
```

---

## STEP 4: Configure Cloud Run Secrets

### 4.1 Create Secret Manager
```powershell
# Set these with your actual values
$LIVEKIT_URL = "wss://friday-uk2toy5r.livekit.cloud"
$LIVEKIT_API_KEY = "APIYnzgriSNVjbG"
$LIVEKIT_API_SECRET = "0nICJFFHqmYECGsZ31pUR3EE98KUxaUbPlfPC4IFirX"
$GOOGLE_API_KEY = "your_google_api_key"
$GMAIL_PASSWORD = "your_gmail_app_password"
$GMAIL_USER = "your_email@gmail.com"
```

### 4.2 Create Secrets in GCP
```powershell
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secrets (run these one by one)
echo $LIVEKIT_URL | gcloud secrets create LIVEKIT_URL --data-file=-
echo $LIVEKIT_API_KEY | gcloud secrets create LIVEKIT_API_KEY --data-file=-
echo $LIVEKIT_API_SECRET | gcloud secrets create LIVEKIT_API_SECRET --data-file=-
echo $GOOGLE_API_KEY | gcloud secrets create GOOGLE_API_KEY --data-file=-
echo $GMAIL_PASSWORD | gcloud secrets create GMAIL_APP_PASSWORD --data-file=-
echo $GMAIL_USER | gcloud secrets create GMAIL_USER --data-file=-
```

### 4.3 Grant Cloud Run Service Permission
```powershell
# Get your project number
$PROJECT_NUMBER = gcloud projects describe friday-jarvis --format='value(projectNumber)'
echo "Project Number: $PROJECT_NUMBER"

# Grant Secret Accessor role
gcloud secrets add-iam-policy-binding LIVEKIT_URL --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding LIVEKIT_API_KEY --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding LIVEKIT_API_SECRET --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding GMAIL_APP_PASSWORD --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding GMAIL_USER --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
```

---

## STEP 5: Build and Push Docker Image

### 5.1 Configure Docker Authentication
```powershell
# Configure gcloud as Docker credential helper
gcloud auth configure-docker gcr.io
```

### 5.2 Get Your Project ID
```powershell
$PROJECT_ID = gcloud config get-value project
echo "Project ID: $PROJECT_ID"
```

### 5.3 Build Docker Image
```powershell
cd C:\Users\paull\Desktop\friday_jarvis

# Build the image (this takes 3-5 minutes)
docker build -t gcr.io/$PROJECT_ID/friday-jarvis:latest .
```

**What this does:**
- Creates Docker image from your Dockerfile
- Names it for Google Container Registry
- Installs all Python dependencies
- Prepares your code for deployment

### 5.4 Push Image to Google Container Registry
```powershell
docker push gcr.io/$PROJECT_ID/friday-jarvis:latest
```

**What this does:**
- Uploads image to Google's container registry
- Takes 1-3 minutes depending on connection

### 5.5 Verify Image Uploaded
```powershell
gcloud container images list --repository=gcr.io/$PROJECT_ID
```

Should show:
```
gcr.io/friday-jarvis/friday-jarvis
```

---

## STEP 6: Deploy to Cloud Run

### 6.1 Deploy Service
```powershell
gcloud run deploy friday-jarvis `
  --image gcr.io/$PROJECT_ID/friday-jarvis:latest `
  --region us-central1 `
  --memory 512Mi `
  --cpu 1 `
  --timeout 3600 `
  --set-env-vars "^|^LIVEKIT_URL=wss://friday-uk2toy5r.livekit.cloud|LIVEKIT_API_KEY=APIYnzgriSNVjbG|LIVEKIT_API_SECRET=0nICJFFHqmYECGsZ31pUR3EE98KUxaUbPlfPC4IFirX" `
  --no-allow-unauthenticated
```

**Explanations:**
- `--image` - Docker image to deploy
- `--region us-central1` - Server location (adjust if needed)
- `--memory 512Mi` - RAM allocated (sufficient for Python agent)
- `--cpu 1` - CPU cores
- `--timeout 3600` - Allow long-running connections (1 hour)
- `--no-allow-unauthenticated` - Require auth token (secure)

### 6.2 When Prompted
```
Allow unauthenticated invocations to [friday-jarvis] (y/N)? N
```
Type: `N` (No) - Keep it secure

### 6.3 Wait for Deployment
```
Deploying container to Cloud Run service [friday-jarvis] in region [us-central1]
✓ Deploying new service... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
Done!
Service [friday-jarvis] revision [friday-jarvis-00001] has been deployed
```

---

## STEP 7: Get Service URL and Auth Token

### 7.1 Get Service URL
```powershell
gcloud run services describe friday-jarvis --region us-central1 --format='value(status.url)'
```

Example output:
```
https://friday-jarvis-abc123xyz-uc.a.run.app
```

Save this URL - your Android app will connect here.

### 7.2 Get Auth Token for Testing
```powershell
gcloud auth print-access-token
```

Save this token - needed for authentication.

---

## STEP 8: Configure Android App

### 8.1 Update TokenExt.kt
In `Maya\app\src\main\java\io\livekit\android\example\voiceassistant\TokenExt.kt`:

```kotlin
package io.livekit.android.example.voiceassistant

const val sandboxID = ""  // Keep empty since using custom backend

const val hardcodedUrl = "https://friday-jarvis-abc123xyz-uc.a.run.app"  // Your Cloud Run URL

const val hardcodedToken = "ya29.your-access-token-here"  // Auth token from Step 7.2
```

### 8.2 Rebuild APK
```powershell
cd C:\Users\paull\Desktop\friday_jarvis\Maya
./gradlew assembleRelease
```

APK location: `Maya\app\build\outputs\apk\release\app-release.apk`

---

## STEP 9: Verify Deployment

### 9.1 Check Cloud Run Logs
```powershell
gcloud run logs read friday-jarvis --region us-central1 --limit 50
```

Should show your agent starting up with no errors.

### 9.2 Test Backend Connection
```powershell
# Get service URL
$SERVICE_URL = gcloud run services describe friday-jarvis --region us-central1 --format='value(status.url)'

# Get auth token
$AUTH_TOKEN = gcloud auth print-access-token

# Test health check
curl -H "Authorization: Bearer $AUTH_TOKEN" $SERVICE_URL
```

### 9.3 Monitor Real-Time Logs
```powershell
gcloud run logs read friday-jarvis --region us-central1 --follow
```

Keep this running while testing your Android app.

---

## STEP 10: Test with Android App

### 10.1 Install APK on Device
```powershell
adb connect your-device-ip:5555  # if wireless
adb install Maya\app\build\outputs\apk\release\app-release.apk
```

### 10.2 Launch App
- Open Friday JARVIS on Android device
- Go to ConnectScreen
- Tap "[ INITIALIZE CALL ]"
- Grant microphone permission

### 10.3 Monitor Backend
In your terminal with logs running:
```
Agent initialized...
Session connected from: [your-device-ip]
Processing audio...
[Response from Google Realtime LLM]
```

---

## STEP 11: Set Up Auto-Scaling (Optional)

### 11.1 Update Memory/CPU if Needed
```powershell
gcloud run services update friday-jarvis `
  --region us-central1 `
  --memory 1Gi `
  --cpu 2 `
  --min-instances 0 `
  --max-instances 10
```

**Scaling settings:**
- `--min-instances 0` - Scale down to zero when idle (saves money)
- `--max-instances 10` - Allow up to 10 concurrent connections
- Auto-scales based on CPU usage

### 11.2 View Metrics
In Cloud Console:
```
1. Go to Cloud Run
2. Click "friday-jarvis" service
3. Go to "Metrics" tab
4. View CPU, Memory, Request Count
```

---

## STEP 12: Troubleshooting

### Issue: "Deployment failed"
```powershell
# Check build logs
gcloud builds log <BUILD_ID>

# Re-run deployment
gcloud run deploy friday-jarvis ...  # repeat STEP 6
```

### Issue: "Permission denied" errors
```powershell
# Grant Cloud Build permissions
gcloud projects add-iam-policy-binding friday-jarvis `
  --member=serviceAccount:$(gcloud projects describe friday-jarvis --format='value(projectNumber)')@cloudbuild.gserviceaccount.com `
  --role=roles/editor
```

### Issue: Service won't start
```powershell
# Check recent logs
gcloud run logs read friday-jarvis --region us-central1 --limit 100

# Look for: ValueError, ImportError, or configuration issues
# Common fixes:
# - Missing environment variables
# - Wrong LiveKit credentials
# - Missing Python dependencies in requirements.txt
```

### Issue: "Image not found"
```powershell
# Verify image exists
gcloud container images list --repository=gcr.io/$PROJECT_ID

# Re-push if missing
docker push gcr.io/$PROJECT_ID/friday-jarvis:latest
```

---

## STEP 13: Monitor Costs

### Free Tier Benefits
- **2M requests/month** - Free
- **360K GB-seconds/month** - Free (your usage ~10GB-seconds/request)
- **1TB egress/month** - Free

### Estimated Monthly Cost
```
Your agent with 512MB RAM, 1 CPU:
- 100 requests/day = 3,000/month
- At 30 seconds per request = 1,500 GB-seconds
- Cost: $0 (within free tier)

If using 1GB RAM, 2 CPU:
- Same usage = $2-5/month (after free credits)
```

### View Cost Breakdown
1. Go to Cloud Console
2. Search "Billing"
3. Go to "Costs" tab
4. Filter by "Cloud Run"

---

## STEP 14: Production Checklist

- [ ] Docker image builds successfully
- [ ] All secrets configured in Secret Manager
- [ ] Cloud Run service deployed and running
- [ ] Logs show no errors
- [ ] Android app connects successfully
- [ ] Agent responds to voice input
- [ ] Tools (weather, search, email) execute
- [ ] Auto-scaling configured (min 0, max 10)
- [ ] Monitoring alerts set up (optional)
- [ ] Backup strategy for secrets

---

## Quick Reference Commands

```powershell
# Deploy
gcloud run deploy friday-jarvis --image gcr.io/$PROJECT_ID/friday-jarvis:latest --region us-central1 --memory 512Mi --cpu 1 --timeout 3600 --no-allow-unauthenticated

# View logs
gcloud run logs read friday-jarvis --region us-central1 --follow

# Get service URL
gcloud run services describe friday-jarvis --region us-central1 --format='value(status.url)'

# Update deployment
gcloud run services update friday-jarvis --region us-central1 --memory 1Gi

# Delete service (if needed)
gcloud run services delete friday-jarvis --region us-central1

# View all services
gcloud run services list --region us-central1
```

---

## Support & Next Steps

**After Successful Deployment:**
1. Test with multiple concurrent users
2. Monitor logs for errors
3. Optimize memory/CPU if needed
4. Set up alerting for failures
5. Implement traffic routing (canary deployments)

**Scaling Beyond Free Tier:**
- Upgrade to Firebase Blaze plan for more quota
- Use Cloud Tasks for background jobs
- Implement request queuing for spikes

**Security Improvements:**
- Use Cloud Armor for DDoS protection
- Enable VPC for private networking
- Rotate secrets regularly
- Implement API key rotation

---

**Estimated Total Time: 30-45 minutes**

Let me know when you're ready to start! 🚀
