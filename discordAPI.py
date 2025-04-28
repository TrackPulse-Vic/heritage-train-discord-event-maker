import asyncio
import os
from dotenv import load_dotenv
from eventAPI import DiscordEvents

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")

discord_events = DiscordEvents(TOKEN)

async def readEvents(gid):
    events = await discord_events.list_guild_events(gid)
    return events    
async def addEvent(guild_id: str,
        event_name: str,
        event_description: str,
        event_start_time: str,
        event_end_time: str,
        event_metadata: dict,
        event_privacy_level=2,
        channel_id=None):
    await discord_events.create_guild_event(guild_id, event_name, event_description, event_start_time, event_end_time, event_metadata, event_privacy_level, channel_id)
   
