import asyncio
from discordAPI import addEvent
from eventAPI import DiscordEvents
from parser import parse_events
from scraper import *
import re
from dotenv import load_dotenv
import os
import csv

async def addEventsToServer():
    print("Welcome to the Scraper!")
    print('We are setting up the Discord API for you.')
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    SERVER = os.getenv('SERVER_ID')

    if not TOKEN:
        raise ValueError("DISCORD_TOKEN not found in .env file")
    if not SERVER:
        raise ValueError("SERVER_ID not found in .env file")

    discord_events = DiscordEvents(TOKEN)


    print("We are scraping the Steamrail website for you.")

    steamrail = steamrail_tours()
    print(steamrail)

    parsed_data = parse_events(steamrail)

    # Print the results in a readable format
    for event in parsed_data:
        print(f"\nDate: {event['date']}")
        print(f'End: {event["end_date"]}')
        print(f"Name: {event['name']}")
        print(f"Type: {event['type']}")
        print(f"Description: {event['description']}")
        print(f"Book link: {event['book_link']}")
        

    print("We are now adding the events to the Discord server.")


    # File to store added events
    EVENTS_FILE = f'servers/{SERVER}.csv'

    # Create the CSV file if it doesn't exist
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['event_name'])

    # Read existing events
    existing_events = set()
    with open(EVENTS_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        existing_events = {row[0] for row in reader}

    for event in parsed_data:
        # Skip if event already exists
        if event['name'] in existing_events:
            print(f"Event {event['name']} already exists, skipping.")
            continue

        # Add the event to the Discord server
        if event['book_link'] != None:
            try:
                await addEvent(SERVER, event['name'], event['description'], event['date'], event["end_date"], {'location': event['book_link']})
                with open(EVENTS_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([event['name']])
                    print(f"Successfully added event: {event['name']}")
            except Exception as e:
                print(f"Error adding event: {e}")
        else:
            print(f"Event {event['name']} has no book link, skipping.")
        
        time.sleep(2)  # Add a delay to avoid rate limiting
        
        # break  # Remove this line to add all events
