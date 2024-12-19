# p
# Import necessary packages=============================================
import random

import psycopg2  # type: ignore
import re  # Necessary for the conv_names function
import time
import json
import requests
from bs4 import BeautifulSoup


# ======================================================================
# Tools

def get_wait_time(quick=True):
    if quick:
        return random.uniform(17, 31)
    else:
        return random.uniform(30, 60)


# ======================================================================
# SCRAPER OPERATION

def run_scrape():
    try:  # Iterate through each page of recipes and scrape recipe elements
        page_num = 0
        while True:
            page_num += 1
            url = f"https://www.diffordsguide.com/cocktails/search?s=1&isrc=browse&ificm=1&ifipp=1&g%5Bdg%5D=1&gid=all&na=1&p={page_num}"
            page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(page.content, "html.parser")

            results = soup.find(id="content-container")
            print(results.prettify())
            time.sleep(get_wait_time())
            quit(42) # temporary
    except:
        print(f"Scraped {page_num} pages.")


# ======================================================================
# MAIN FUNCTION

if __name__ == "__main__":
    run_scrape()
