# 🤖 Friday - AI Voice Assistant

A powerful AI voice assistant built with LiveKit, featuring real-time voice interactions, web search, weather updates, and email capabilities.


## 🛠️ Technical Details

### Architecture
- **Backend**: FastAPI with LiveKit Agents
- **Voice AI**: Google Gemini Realtime API
- **Real-time Communication**: LiveKit WebRTC
- **Tools**: Weather API, DuckDuckGo Search, Gmail SMTP

### Environment Variables Required
```
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
GOOGLE_API_KEY=your-google-ai-api-key
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
```

## 📱 Mobile App Integration

### iOS (Swift)
```swift
import LiveKit

// Connect to Friday's room
let room = Room()
let options = ConnectOptions()
try await room.connect("wss://your-hf-space.hf.space/livekit", token: token)
```

### Android (Kotlin)
```kotlin
import io.livekit.android.room.Room

// Connect to Friday's room
val room = Room()
room.connect("wss://your-hf-space.hf.space/livekit", token)
```

### Web Integration
```javascript
// Get room token
const response = await fetch('/token?roomName=my-room&identity=user123');
const data = await response.json();

// Connect with LiveKit client
const room = new LivekitClient.Room();
await room.connect('wss://your-hf-space.hf.space/livekit', data.token);
```

## 🔧 API Endpoints

### Web/Mobile App Integration

#### Create Room
```
POST /create-room
Response: { "success": true, "room_name": "room-abc123", "livekit_url": "..." }
```

#### Get Access Token
```
GET /token?roomName=room-abc123&identity=user123
Response: { "token": "jwt-token-here" }
```

#### Health Check
```
GET /health
Response: { "status": "healthy", "service": "Friday AI Assistant" }
```

#### Get Configuration
```
GET /api/config
Response: { "livekit_url": "...", "features": { ... } }
```

## 🏗️ Development

### Local Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run: `python app.py`

```bash
python .\agent.py  console  to run on the terminal.
python .\agent.py  dev  to connect to your livekit playground.
docker build -t friday-voice-assistant .
docker run -p 7860:7860 friday-voice-assistant
```

## 📋 Requirements

- Python 3.12+
- LiveKit Cloud account
- Google AI Studio API key
- Gmail account (for email features)

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.


---

**Built with ❤️by LINCOLN PAUL**