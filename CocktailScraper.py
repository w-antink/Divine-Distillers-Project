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

def run_scrape():# Iterate through each page of recipes and scrape recipe contents
    try:
        page_num = 0
        while page_num<1:
            page_num += 1
            url = f"https://www.diffordsguide.com/cocktails/search?s=1&isrc=browse&ificm=1&ifipp=1&g%5Bdg%5D=1&gid=all&na=1&p={page_num}"
            page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="content-container")
            recipe_cards = results.find_all("div", class_="cell small-6 medium-3 large-2")

            for recipe_card in recipe_cards:
                title = recipe_card.find("h3", class_="link-box__title").get_text(strip=True)
                ingredients = [i.select_one("div.link-box__ingredient-name").get_text(strip=True) for i in recipe_card.select("div.link-box__ingredient")]
            print(title, ingredients)

            #time.sleep(get_wait_time()) #temporary comment
            #quit(42) #temporary comment
    except:
        print(f"Scraped {page_num} pages.")

def clean_scrape(): #Clean and standardize data from scrape before storage
    pass
# ======================================================================
# MAIN FUNCTION

if __name__ == "__main__":
    run_scrape()

# ======================================================================
#NOTES AND TO-DO'S

#Remove recipe tags as neccessary.
#Trim and generalize ingredient names (ugh)
#Figure out cleaning requirements
#Figure out and implement storage

#CONSIDERATIONS

#Should clean in batches? Or as we go?
#Do we want to store in a DB, or is a dataframe fine?
#How do we feel about using *this* data/source?
#Should we containerize the scrape and cleaning processes and have them run on railway?
