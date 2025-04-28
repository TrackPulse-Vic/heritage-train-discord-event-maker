import datetime
import re

def parse_events(events_list):
    """
    Parse event information from a list of dictionaries containing event content and booking links.
    Returns a list of dictionaries containing date, name, description, type, and book_link for each event.
    """
    parsed_events = []
    
    for event in events_list:
        content = event['content']
        # Split the initial date and rest of the content
        date_split = content.split('– ', 1)
        if len(date_split) != 2:
            continue
            
        raw_date, content = date_split
        
        # Clean up the date
        raw_date = raw_date.strip().replace('\xa0', ' ')
        
        # Parse the date
        try:
            date_obj = datetime.datetime.strptime(raw_date, '%A %dth %B %Y')
        except ValueError:
            try:
                date_obj = datetime.datetime.strptime(raw_date, '%A %dst %B %Y')
            except ValueError:
                try:
                    date_obj = datetime.datetime.strptime(raw_date, '%A %dnd %B %Y')
                except ValueError:
                    try:
                        date_obj = datetime.datetime.strptime(raw_date, '%A %drd %B %Y')
                    except ValueError:
                        # Handle date ranges
                        if '-' in raw_date:
                            start_date = raw_date.split('-')[0].strip()
                            try:
                                date_obj = datetime.datetime.strptime(start_date, '%A %dth %B %Y')
                            except ValueError:
                                continue
                        else:
                            continue

        # Set time to be an estimation based on what they normally do
        # Convert to Australian Eastern Standard Time (AEST, UTC+10)
        date_obj = date_obj.replace(hour=10, minute=0, second=0)  # Set start time to 10am AEST
        formatted_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S+10:00')

        # For end time, set to 6pm same day
        date_obj_later = date_obj.replace(hour=18)  # Set end time to 6pm AEST
        formatted_date_later = date_obj_later.strftime('%Y-%m-%dT%H:%M:%S+10:00')
        
        
        # Split content into name and description
        # Event type is typically in parentheses (S), (D), (E), etc.
        name_match = re.match(r'([^(]+)\s*(\([^)]+\))?\s*', content)
        if name_match:
            event_name = name_match.group(1).strip()
            event_type = name_match.group(2) if name_match.group(2) else ''
            
            # Everything after the name and type is the description
            description_start = len(name_match.group(0))
            description = content[description_start:].strip()
            
            # Clean up the description
            description = description.replace('\xa0', ' ').strip()
            # Remove "Book Now | RSVP on Facebook" if present
            description = re.sub(r'Book Now\s*\|\s*RSVP on Facebook\ufeff?', '', description).strip()
            
            parsed_events.append({
                'date': formatted_date,
                'end_date': formatted_date_later,
                'name': event_name,
                'type': event_type,
                'description': description,
                'book_link': event['book_link']
            })
    
    return parsed_events

def parseSevenOsevenEvents(events):
    parsed_events = []
    
    for event in events:
        content = event['content']
        # Extract date using regex for different formats
        date_match = re.search(r'(\d{1,2})\s+([A-Za-z]+)(?:\s+to\s+(\d{1,2})\s+([A-Za-z]+))?,?\s+(\d{4})', content)
        if not date_match:
            continue

        start_day, start_month, end_day, end_month, year = date_match.groups()
        start_date_str = f"{start_day} {start_month} {year}"

        try:
            start_date_obj = datetime.datetime.strptime(start_date_str, '%d %B %Y')
            # Set start time to 10am AEST
            start_date_obj = start_date_obj.replace(hour=10, minute=0, second=0)
            formatted_date = start_date_obj.strftime('%Y-%m-%dT%H:%M:%S+10:00')
            
            # If end_day exists, use it for end_date, otherwise use start_day
            if end_day:
                # Use end_month if provided, otherwise use start_month
                month_to_use = end_month if end_month else start_month
                end_date_str = f"{end_day} {month_to_use} {year}"
                end_date_obj = datetime.datetime.strptime(end_date_str, '%d %B %Y')
                end_date_obj = end_date_obj.replace(hour=18, minute=0, second=0)
            else:
                end_date_obj = start_date_obj.replace(hour=18)
            
            formatted_date_later = end_date_obj.strftime('%Y-%m-%dT%H:%M:%S+10:00')

            # Extract name and description (rest of the content)
            name_match = re.match(r'.*?\d{4}\s*[-–]\s*([^-–]+)', content)
            
            parsed_events.append({
                'date': formatted_date,
                'end_date': formatted_date_later,
                'name': event.get('name'),
                'description': content,
                'book_link': event.get('book_link')
            })
        except ValueError:
            continue

    return parsed_events

