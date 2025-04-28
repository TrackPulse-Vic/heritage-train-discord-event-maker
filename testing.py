from dotenv import load_dotenv
from ical import make_icalender
from parser import parse_events, parseSevenOsevenEvents
from scraper import steamrail_tours, sevenOseven_tours

print(parse_events(sevenOseven_tours()))