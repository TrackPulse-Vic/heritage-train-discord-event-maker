import asyncio
import uuid

from discordAPI import addEvent
from eventAPI import DiscordEvents
from ical import make_icalender
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
    
    sevenOseven = sevenOseven_tours()
    print(sevenOseven)

    steamrail_parsed = parse_events(steamrail)
    sevenOseven_parsed = parseSevenOsevenEvents(sevenOseven)
    parsed_data = steamrail_parsed + sevenOseven_parsed

    # Print the results in a readable format
    for event in parsed_data:
        print(f"\nDate: {event['date']}")
        print(f'End: {event["end_date"]}')
        print(f"Name: {event['name']}")
        # print(f"Type: {event['type']}")
        print(f"Description: {event['description']}")
        print(f"Book link: {event['book_link']}")
        
        # shorten description to 100 characters
        if len(event['name']) > 100:
            event['name'] = event['name'][:90] + '...'
        # shorten url if its 707 cause their ones are too long for discord
        if event['book_link'].startswith('https://www.slowrailjourneys.com.au'):
            urlShortened = 'https://www.slowrailjourneys.com.au'
        else:
            urlShortened = event['book_link']
    
    print('We are now making calender files for each event.')
    for event in parsed_data:
        make_icalender(event['date'], event['end_date'], event['name'], event['description'], event['book_link'])
        

    print("We are now adding the events to the Discord server.")


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

    newEvents = []
    for event in parsed_data:
        # Skip if event already exists
        if event['name'] in existing_events:
            print(f"Event {event['name']} already exists, skipping.")
            continue

        # Add the event to the Discord server
        if event['book_link'] != None:
            try:
                worked = await addEvent(SERVER, event['name'], event['description'], event['date'], event["end_date"], {'location': urlShortened})
                if worked:
                    with open(EVENTS_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([event['name']])
                        print(f"Successfully added event: {event['name']}")
                    newEvents.append((event['name'], event['book_link']))
                else:
                    print(f"Failed to add event: {event['name']}")
                
            except Exception as e:
                print(f"Error adding event: {e}")
        else:
            print(f"Event {event['name']} has no book link, skipping.")
        
        time.sleep(10)  # avoid rate limiting
        
    return newEvents
