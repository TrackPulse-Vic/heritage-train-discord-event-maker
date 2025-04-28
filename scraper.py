from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from parser import parseSevenOsevenEvents

def steamrail_tours():
    url = 'https://www.steamrail.com.au/tours'

    # Set up Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')

    # Initialize the Firefox driver
    print('Starting Scraper')
    driver = webdriver.Firefox(options=firefox_options)

    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for dynamic content to load
        time.sleep(3)  # Adjust this delay if needed
        
        # Get the page source after JavaScript execution
        page_source = driver.page_source
        
        # Parse with BeautifulSoup
        print('Reading Page')
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the container div
        print('Finding Events')
        container = soup.find('div', {'class': 'w-container col'})
        
        # Find all divs with specific class within the container
        print('Reading Events')
        content_divs = container.find_all('div', {'class': 'w-cell text-image-row row'}) if container else []
        
        # Store both text content and book now links
        items = []
        for div in content_divs:
            text_content = div.text.strip()
            book_now_link = None
            link = div.find('a', string='Book Now')
            if link:
                book_now_link = link.get('href')
            
            if text_content:
                items.append({
                    'content': text_content,
                    'book_link': book_now_link
                })
            
        return items

    finally:
        # Clean up
        driver.quit()
        print('Steamrail Scraper Finished')

def sevenOseven_tours():
    url = 'https://www.707operations.com.au'
    
    # Set up Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')

    # Initialize the Firefox driver
    print('Starting Scraper')
    driver = webdriver.Firefox(options=firefox_options)

    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for dynamic content to load
        # time.sleep(3)  # Adjust this delay if needed
        
        # Get the page source after JavaScript execution
        page_source = driver.page_source
        
        # Parse with BeautifulSoup
        print('Reading Page')
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the container div
        print('Finding Events')
        # Find the <h2> that says "Upcoming journeys with our moving museum:"
        upcoming_section = soup.find('h2', string=lambda text: text and "Upcoming journeys with our moving museum:" in text)

        # List to store found h1s
        events = []

        if upcoming_section:
            # Find the first div after the h2
            sibling_div = upcoming_section.find_next_sibling('div')
            if sibling_div:
                # Now find all h1 tags inside *any* level inside that div
                events = sibling_div.find_all('h1')
        
        # Store both text content and book now links
        items = []
        for event in events:
            text_content = event.text.strip()
            book_now_link = None
            link = event.find('a')
            if link:
                book_now_link = link.get('href')
                name = link.text
            
            if text_content:
                items.append({
                    'name': name,
                    'content': text_content,
                    'book_link': book_now_link
                })
            
        return items

    finally:
        # Clean up
        driver.quit()
        print('707 Scraper Finished')