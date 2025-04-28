import os
import icalendar
import datetime

def make_icalender(start_time_str, end_time_str, title, description, location):
    """
    Create an iCalendar event.

    Args:
        start_time_str (str): Start time in ISO format (e.g., '2025-02-09T10:00:00+10:00')
        end_time_str (str): End time in ISO format (e.g., '2025-02-09T10:00:00+10:00')
        title (str): The title of the event.
        description (str): The description of the event.
        location (str): The location of the event.

    Returns:
        str: The path to the created .ics file.
    """
    cal = icalendar.Calendar()
    event = icalendar.Event()
    
    start_time = datetime.datetime.fromisoformat(start_time_str)
    end_time = datetime.datetime.fromisoformat(end_time_str)
    
    event.add('summary', title)
    event.add('description', description)
    event.add('location', location)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)

    # Add the event to the calendar
    cal.add_component(event)
    path = os.path.join('events/', f'{title}.ics')
    
    f = open(path, 'wb')
    f.write(cal.to_ical())

    return path