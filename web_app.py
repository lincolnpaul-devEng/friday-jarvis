import os
import uuid
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import logging

try:
    from livekit.api import AccessToken, VideoGrant
except ImportError:
    # Fallback for older versions
    from livekit import AccessToken, VideoGrant

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://friday-uk2toy5r.livekit.cloud")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/create-room', methods=['POST'])
def create_room():
    """Create a new LiveKit room"""
    try:
        room_name = f"room-{str(uuid.uuid4())[:8]}"
        logger.info(f"Created room: {room_name}")
        return jsonify({
            'success': True,
            'room_name': room_name,
            'livekit_url': LIVEKIT_URL
        })
    except Exception as e:
        logger.error(f"Error creating room: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/join-room/<room_name>')
def join_room(room_name):
    """Serve room interface"""
    return render_template('room.html', room_name=room_name, livekit_url=LIVEKIT_URL)

@app.route('/token')
def get_token():
    """Generate LiveKit access token for client"""
    try:
        room_name = request.args.get('roomName', 'default-room')
        identity = request.args.get('identity', f'user-{uuid.uuid4().hex[:8]}')

        # Create access token
        token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        token.identity = identity
        token.name = identity

        # Grant permissions
        grant = VideoGrant()
        grant.room = room_name
        grant.room_join = True
        grant.can_publish = True
        grant.can_subscribe = True
        grant.can_publish_data = True

        token.video_grant = grant

        jwt_token = token.to_jwt()
        return jsonify({'token': jwt_token})
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)