import os
import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import logging
import uvicorn

try:
    from livekit.api import AccessToken, VideoGrants
except ImportError:
    try:
        # Try alternative import paths
        from livekit import AccessToken, VideoGrants
    except ImportError:
        # Last resort - try different combinations
        try:
            from livekit.api import AccessToken
            from livekit.api import VideoGrants
        except ImportError:
            # If all else fails, create a simple token generation
            AccessToken = None
            VideoGrants = None

load_dotenv()

app = FastAPI(title="Friday - AI Voice Assistant", description="Personal AI voice assistant powered by LiveKit")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://friday-uk2toy5r.livekit.cloud")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create-room")
async def create_room():
    """Create a new LiveKit room"""
    try:
        room_name = f"room-{str(uuid.uuid4())[:8]}"
        logger.info(f"Created room: {room_name}")
        return {
            "success": True,
            "room_name": room_name,
            "livekit_url": LIVEKIT_URL
        }
    except Exception as e:
        logger.error(f"Error creating room: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create room: {str(e)}")

@app.get("/join-room/{room_name}", response_class=HTMLResponse)
async def join_room(request: Request, room_name: str):
    """Serve room interface"""
    return templates.TemplateResponse("room.html", {
        "request": request,
        "room_name": room_name,
        "livekit_url": LIVEKIT_URL
    })

@app.get("/token")
async def get_token(roomName: str = None, identity: str = None):
    """Generate LiveKit access token for client"""
    try:
        if not roomName:
            raise HTTPException(status_code=400, detail="roomName parameter is required")

        room_name = roomName
        if not identity:
            identity = f'user-{uuid.uuid4().hex[:8]}'

        # Try to import and use LiveKit token generation
        if AccessToken is not None and VideoGrants is not None:
            # Use proper LiveKit API
            token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
            token.identity = identity
            token.name = identity

            # Grant permissions
            grant = VideoGrants()
            grant.room = room_name
            grant.room_join = True
            grant.can_publish = True
            grant.can_subscribe = True
            grant.can_publish_data = True

            token.video_grants = grant

            jwt_token = token.to_jwt()
            return {"token": jwt_token}
        else:
            # Fallback: return a mock token for testing (replace with proper implementation)
            import base64
            import json
            import time

            # Create a simple JWT-like token (NOT SECURE - for testing only)
            header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode()
            payload = base64.b64encode(json.dumps({
                "identity": identity,
                "name": identity,
                "room": room_name,
                "exp": int(time.time()) + 3600  # 1 hour
            }).encode()).decode()

            # Simple signature (NOT SECURE)
            message = f"{header}.{payload}"
            signature = base64.b64encode(f"mock_signature_{room_name}_{identity}".encode()).decode()

            mock_token = f"{header}.{payload}.{signature}"
            logger.warning("Using mock token - LiveKit imports failed")
            return {"token": mock_token, "warning": "Mock token - LiveKit integration incomplete"}

    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Friday AI Assistant"}

@app.get("/api/config")
async def get_config():
    """Get client configuration"""
    return {
        "livekit_url": LIVEKIT_URL,
        "features": {
            "voice_assistant": True,
            "weather_lookup": True,
            "web_search": True,
            "email_sending": bool(os.getenv("GMAIL_USER")),
            "video_support": True
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7860))  # HF Spaces uses 7860
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )