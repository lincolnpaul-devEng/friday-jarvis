from dotenv import load_dotenv
import logging

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, send_email

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.7,
                # Increase timeout for Gemini API connection
                # Default is often too short for initial handshake
                timeout=30.0,  # 30 seconds for connection
            ),
            tools=[
                get_weather,
                search_web,
                send_email
            ],
        )
        


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession()
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"Starting agent session (attempt {retry_count + 1}/{max_retries})")
            
            await session.start(
                room=ctx.room,
                agent=Assistant(),
                room_input_options=RoomInputOptions(
                    # LiveKit Cloud enhanced noise cancellation
                    # - If self-hosting, omit this parameter
                    # - For telephony applications, use `BVCTelephony` for best results
                    video_enabled=True,
                    noise_cancellation=noise_cancellation.BVC(),
                ),
            )

            await ctx.connect()
            logger.info("Agent session started successfully")
            break  # Success, exit retry loop
            
        except Exception as e:
            retry_count += 1
            logger.error(f"Agent session error: {e}")
            
            if retry_count < max_retries:
                import asyncio
                wait_time = 5 * retry_count  # Exponential backoff: 5s, 10s, 15s
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"Failed to start agent session after {max_retries} attempts")
                raise

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))