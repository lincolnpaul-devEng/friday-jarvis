# 🚀 Friday AI Assistant - Heroku Deployment Guide

This guide will help you deploy the Friday AI voice assistant to Heroku and ensure it's properly configured for web and mobile access.

## 📋 Prerequisites

Before deploying, ensure you have:

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure you have Git installed
4. **Valid API Keys**: All required API keys (see Environment Variables section)

## 🛠️ Step 1: Prepare Your Application

### 1.1 Ensure All Files Are Present

Your project should have these files:
- `agent.py` - The main LiveKit agent
- `web_app.py` - Flask web application
- `tools.py` - Agent tools (weather, search, email)
- `prompts.py` - Agent instructions
- `Procfile` - Heroku process definitions
- `runtime.txt` - Python version specification
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `.env` - Environment variables (for local development)

### 1.2 Update API Keys

**CRITICAL**: Your current Google API key has been flagged as leaked. You need a new one:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Update your `.env` file with the new key

## 🌐 Step 2: Set Up LiveKit Cloud (Required)

The voice agent requires LiveKit Cloud for real-time communication:

1. **Sign up for LiveKit Cloud**: Visit [cloud.livekit.io](https://cloud.livekit.io)
2. **Create a project**: Get your `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`
3. **Note your LiveKit URL**: Usually `wss://your-project.livekit.cloud`

## 🚀 Step 3: Deploy to Heroku

### 3.1 Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit - Friday AI Assistant"
```

### 3.2 Create Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add buildpacks (in order)
heroku buildpacks:add heroku/python
```

### 3.3 Configure Environment Variables

Set all required environment variables on Heroku:

```bash
# LiveKit Configuration (REQUIRED)
heroku config:set LIVEKIT_URL="wss://your-project.livekit.cloud"
heroku config:set LIVEKIT_API_KEY="your-livekit-api-key"
heroku config:set LIVEKIT_API_SECRET="your-livekit-api-secret"

# Google AI (REQUIRED - get new key!)
heroku config:set GOOGLE_API_KEY="your-new-google-api-key"

# Gmail Configuration (OPTIONAL - for email tool)
heroku config:set GMAIL_USER="your-email@gmail.com"
heroku config:set GMAIL_APP_PASSWORD="your-gmail-app-password"

# OpenRouter (OPTIONAL - backup LLM)
heroku config:set OPENROUTER_API_KEY="your-openrouter-key"
```

### 3.4 Deploy

```bash
# Push to Heroku
git push heroku main

# Scale the dynos
heroku ps:scale web=1 worker=1
```

## 🔍 Step 4: Verify Deployment

### 4.1 Check App Status

```bash
# Check if app is running
heroku ps

# View logs
heroku logs --tail

# Open the app
heroku open
```

### 4.2 Test the Application

1. **Web Interface**: Visit your Heroku app URL
2. **Create Room**: Click "Start Voice Conversation"
3. **Test Voice**: Allow microphone access and speak to Friday
4. **Test Tools**:
   - "What's the weather in London?"
   - "Search for Python tutorials"
   - "Send an email to test@example.com with subject 'Test' and message 'Hello'"

### 4.3 Health Check

Visit `https://your-app-name.herokuapp.com/health` to verify the app is responding.

## 📱 Step 5: Mobile App Access

### 5.1 Using LiveKit Mobile SDKs

For mobile apps, use LiveKit's native SDKs:

**iOS (Swift):**
```swift
import LiveKit

let room = Room()
let options = ConnectOptions()
try await room.connect("wss://your-project.livekit.cloud", token)
```

**Android (Kotlin):**
```kotlin
import io.livekit.android.room.Room

val room = Room()
room.connect("wss://your-project.livekit.cloud", token)
```

### 5.2 Getting Room Tokens

Mobile apps need to request tokens from your server:

```javascript
// Request token from your Heroku app
const response = await fetch('https://your-app-name.herokuapp.com/token?roomName=my-room&identity=user123');
const data = await response.json();
const token = data.token;
```

## 🐛 Troubleshooting

### Common Issues:

**1. Application Crashes on Startup**
- Check logs: `heroku logs --tail`
- Verify all environment variables are set
- Ensure API keys are valid

**2. Voice Agent Not Responding**
- Check if worker dyno is running: `heroku ps`
- Verify LiveKit credentials
- Check Google API key isn't leaked

**3. WebRTC Connection Issues**
- Ensure LiveKit Cloud project is active
- Check firewall settings
- Verify tokens are generated correctly

**4. Tools Not Working**
- Email: Verify Gmail credentials and app password
- Weather: Should work automatically
- Search: Should work automatically

### Debug Commands:

```bash
# View recent logs
heroku logs -n 100

# Check environment variables
heroku config

# Restart app
heroku restart

# Run commands on Heroku
heroku run bash
```

## 🔧 Configuration Options

### Environment Variables Reference:

| Variable | Required | Description |
|----------|----------|-------------|
| `LIVEKIT_URL` | ✅ | LiveKit Cloud WebSocket URL |
| `LIVEKIT_API_KEY` | ✅ | LiveKit API Key |
| `LIVEKIT_API_SECRET` | ✅ | LiveKit API Secret |
| `GOOGLE_API_KEY` | ✅ | Google AI Studio API Key |
| `GMAIL_USER` | ❌ | Gmail address for email tool |
| `GMAIL_APP_PASSWORD` | ❌ | Gmail App Password |
| `OPENROUTER_API_KEY` | ❌ | Backup LLM API key |

### Scaling:

```bash
# Scale web dynos (handles HTTP requests)
heroku ps:scale web=1

# Scale worker dynos (runs the agent)
heroku ps:scale worker=1

# For high traffic, you might need more workers
heroku ps:scale worker=3
```

## 📊 Monitoring

### Heroku Metrics:
- **Dyno Status**: `heroku ps`
- **Logs**: `heroku logs --tail`
- **Metrics**: Heroku Dashboard → Metrics

### Application Health:
- Health endpoint: `/health`
- Agent status: Check worker logs
- LiveKit dashboard: Monitor room connections

## 🔒 Security Considerations

1. **API Keys**: Never commit real API keys to Git
2. **Environment Variables**: Use Heroku config vars for secrets
3. **HTTPS**: Heroku provides SSL automatically
4. **Rate Limiting**: Consider adding rate limits for production
5. **Authentication**: Add user authentication if needed

## 🎯 Next Steps

After successful deployment:

1. **Custom Domain**: Add a custom domain in Heroku settings
2. **CDN**: Consider using Cloudflare for better performance
3. **Monitoring**: Set up error tracking (e.g., Sentry)
4. **Backup**: Regular database backups if using persistent storage
5. **Testing**: Set up automated tests and monitoring

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Heroku logs thoroughly
3. Test API keys locally first
4. Check LiveKit Cloud dashboard
5. Visit [LiveKit Discord](https://discord.gg/livekit) for community support

---

**🎉 Your Friday AI Assistant is now deployed and ready to use!**

Users can access it via web browsers and mobile apps through the LiveKit SDKs. The voice agent will respond to natural language commands and use the available tools for enhanced functionality.