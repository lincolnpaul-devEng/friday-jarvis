#Friday AI Assistant 

## Prerequisites;
-Livekit api keys
-Gemini API key
-Gmail Password
-Gmail user email


## Step 1: Prepare Your Application

### 1.1 Ensure All Files Are Present

Your project should have these files:
- `agent.py` - The main LiveKit agent
- `tools.py` - Agent tools (weather, search, email)
- `prompts.py` - Agent instructions
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `.env` - Environment variables (for local development)

### 1.2 Update API Keys

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Update your `.env` file with the new key

## Step 2: Set Up LiveKit Cloud (Required)

The voice agent requires LiveKit Cloud for real-time communication:

1. **Sign up for LiveKit Cloud**: Visit [cloud.livekit.io](https://cloud.livekit.io)
2. **Create a project**: Get your `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`
3. **Note your LiveKit URL**: Usually `wss://your-project.livekit.cloud`
4.


