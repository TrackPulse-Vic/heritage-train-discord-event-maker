from dotenv import load_dotenv
from ical import make_icalender
from parser import parse_events, parseSevenOsevenEvents
from scraper import steamrail_tours, sevenOseven_tours

def MakeIcal():
    print("Welcome to the Scraper!")
    print("We are scraping the Steamrail website for you.")

    sevenoseven = sevenOseven_tours()
    print(sevenoseven)

    parsed_data = parseSevenOsevenEvents(sevenoseven)

    for event in parsed_data:
        print(f"\nDate: {event['date']}")
        print(f'End: {event["end_date"]}')
        print(f"Name: {event['name']}")
        # print(f"Type: {event['type']}")
        print(f"Description: {event['description']}")
        print(f"Book link: {event['book_link']}")
        
    print('We are now making calender files for each event.')
    for event in parsed_data:
        make_icalender(event['date'], event['end_date'], event['name'], event['description'], event['book_link'])
        
MakeIcal()