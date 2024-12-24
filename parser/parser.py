from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO
import os
import logging
import time



class ParserException(Exception):
    """Custom exception class for parser"""
    def __init__(self, message):
        super().__init__(message)


def init_browser():
    op = webdriver.FirefoxOptions()
    selenium_remote_url = os.getenv('SELENIUM_REMOTE_URL', 'http://localhost:4444')
    attempts = 0
    max_attempts = 10  # Number of attempts to try reconnecting
    sleep_interval = 2  # Seconds to wait between attempts

    while attempts < max_attempts:
        try:
            s = webdriver.Remote(command_executor=selenium_remote_url, options=op)
            return s
        except Exception as e:
            logging.error(f"Attempt {attempts + 1} failed: {e}")
            attempts += 1
            time.sleep(sleep_interval)

    raise Exception("Failed to connect to the Selenium server after multiple attempts")

def parse_page(s, product, region, start, end):
    base_url = 'https://transparencyreport.google.com/traffic/overview?fraction_traffic='
    try:
        url = f"{base_url}start:{start};end:{end};product:{product};region:{region}&lu=fraction_traffic"
        logging.info(f"Fetching: {url}")
        s.get(url)
        logging.info("Loaded")
    except Exception as e:
        logging.error(f"Error loading page: {e}")
        raise ParserException("Can't parse page")

    # Wait for load special CSS-style element
    try:
        wait = WebDriverWait(s, 15)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, r'div[style*="position:absolute; overflow:hidden;left:-10000px; top:auto; width:1px; height:1px;"]')))
        element_html = element.get_attribute('outerHTML')
        logging.info("Element found by CSS")
        # Wrapping HTML code in StringIO
        element_html_io = StringIO(element_html)
        return element_html_io
    except Exception as e:
        logging.error(f"Error waiting for element: {e}")
        raise ParserException("Can't parse page")

def close_browser(s):
    s.quit()
