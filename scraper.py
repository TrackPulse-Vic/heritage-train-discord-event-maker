from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def steamrail_tours():
    url = 'https://www.steamrail.com.au/tours'

    # Set up Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run in headless mode (no GUI)

    # Initialize the Firefox driver
    driver = webdriver.Firefox(options=firefox_options)

    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for dynamic content to load
        time.sleep(3)  # Adjust this delay if needed
        
        # Get the page source after JavaScript execution
        page_source = driver.page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the container div
        container = soup.find('div', {'class': 'w-container col'})
        
        # Find all divs with specific class within the container
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

            