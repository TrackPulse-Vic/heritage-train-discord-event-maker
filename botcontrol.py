from typing import Literal, Optional
from discord.ext import commands, tasks
from discord import app_commands
import discord
import os

from discordAPI import readEvents
from main import addEventsToServer
from datetime import datetime

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('SERVER_ID')
LOG_CHANNEL = 1227224314483576982

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")
if not SERVER:
    raise ValueError("SERVER_ID not found in .env file")

bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    activity = discord.Activity(type=discord.ActivityType.watching, name='for new steamrail events')
    await bot.change_presence(activity=activity)
    task_loop.start()

@tasks.loop(hours=24)
async def task_loop():
    await bot.get_channel(LOG_CHANNEL).send("Refreshing steamrail events...")
    await addEventsToServer()
    await bot.get_channel(LOG_CHANNEL).send("Events steamrail refreshed!")

    
@bot.tree.command(name="refresh", description="Manually refresh the steamrail events")
async def refresh(interaction: discord.Interaction):
    if interaction.user.id == 780303451980038165:
        await interaction.response.send_message("Refreshing steamrail events...")
        try:
            await addEventsToServer()
            await interaction.edit_original_response(content="Steamrail events refreshed!")
        except Exception as e:
            await interaction.edit_original_response(content=f"Error: {e}")
    else:
        await interaction.response.send_message("You don't have permission to do that!")

@bot.tree.command(name='view-events', description='View the upcoming steamrail events')
async def view_events(interaction: discord.Interaction):
    events = await readEvents(SERVER)
    if events:
        # Sort events by scheduled_start_time
        events.sort(key=lambda x: x['scheduled_start_time'])
        
        embed = discord.Embed(title="Upcoming Steamrail Events", color=0xb30303)        
        for event in events:
            # Convert ISO timestamp to Unix timestamp
            dt = datetime.fromisoformat(event['scheduled_start_time'].replace('Z', '+00:00'))
            unix_timestamp = int(dt.timestamp())
            
            embed.add_field(
                name=f"{event['name']} - <t:{unix_timestamp}:D>", 
                value=f"[{event['description']}]({event['entity_metadata']['location']})", 
                inline=False
            )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No upcoming events found!")

# other commands
@bot.tree.command(name="ping", description="Check if bot is responsive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {bot.latency*1000:.2f}ms")
    
@bot.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if ctx.author.id == 780303451980038165:

        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException as e:
                print(f'Error: {e}')
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    

# Replace 'YOUR_TOKEN' with your bot's token
bot.run(TOKEN)