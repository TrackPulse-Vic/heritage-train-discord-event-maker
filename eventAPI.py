'''
Source for the discord event code: https://gist.github.com/adamsbytes/8445e2f9a97ae98052297a4415b5356f
'''

import json

import aiohttp

class DiscordEvents:
    '''Class to create and list Discord events utilizing their API'''
    def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization':f'Bot {discord_token}',
            'User-Agent':'DiscordBot (https://your.bot/url) Python/3.9 aiohttp/3.8.1',
            'Content-Type':'application/json'
        }

    async def list_guild_events(self, guild_id: str) -> list:
        '''Returns a list of upcoming events for the supplied guild ID
        Format of return is a list of one dictionary per event containing information.'''
        event_retrieve_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.get(event_retrieve_url) as response:
                    response.raise_for_status()
                    assert response.status == 200
                    response_list = json.loads(await response.read())
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()
        return response_list

    async def create_guild_event(
        self,
        guild_id: str,
        event_name: str,
        event_description: str,
        event_start_time: str,
        event_end_time: str,
        event_metadata: dict,
        event_privacy_level: int = 2,
        channel_id: str = None
    ) -> None:
        '''Creates a guild event using the supplied arguments
        The expected event_metadata format is event_metadata={'location': 'YOUR_LOCATION_NAME'}
        The required time format is %Y-%m-%dT%H:%M:%SZ (must include Z at the end for UTC)'''
        
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        
        # Base event data
        event_data = {
            'name': event_name,
            'privacy_level': event_privacy_level,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'description': event_description,
            'entity_type': 3,  # 3 represents EXTERNAL event type
            'entity_metadata': event_metadata
        }
        
        # Only include channel_id if it's provided
        if channel_id:
            event_data['channel_id'] = channel_id
        
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(
                    event_create_url, 
                    json=event_data  # Use json parameter instead of data
                ) as response:
                    if response.status == 200:
                        print('Event created successfully')
                    else:
                        error_data = await response.text()
                        print(f'Failed to create event. Status: {response.status}, Error: {error_data}')                    
                        
            except Exception as e:
                print(f'EXCEPTION: {e}')