# p
# Import necessary packages=============================================
import random
import pandas as pd
import psycopg2  # type: ignore
import re  # Necessary for the conv_names function
import time
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# ======================================================================
# Tools

def get_wait_time(quick=True):
    if quick:
        return random.uniform(17, 31)
    else:
        return random.uniform(30, 60)


# ======================================================================
# SCRAPER OPERATION

def get_drinks(soup):

    def get_drink_peliminary_info(soup): # hitlist: name, ingredients (not amounts), url

        # name and url
        # <div class="link-box__head">
        # <h3 class="link-box__title">
        # <a href="/cocktails/recipe/611/daiquiri-diffords-recipe">
        # Daiquiri (Difford's recipe)
        #                  </a>

        name = soup.find("h3", class_="link-box__title").text

        url = soup.find("a", href=True)["href"]
        url = f"https://www.diffordsguide.com{url}"


        # ingredients
        # <div class="link-box__ingredient-name">

        ingredients_raw = soup.find_all("div", class_="link-box__ingredient-name")
        ingredients_raw = [ingredient.text for ingredient in ingredients_raw]
        # remove all \n and \t from ingredients_raw
        ingredients_raw = [re.sub(r"\n|\t", "", ingredient) for ingredient in ingredients_raw]

        return name, url, ingredients_raw


    # find all <div class="cell small-6 medium-3 large-2">
    drinks_raw = soup.find_all("div", class_="cell small-6 medium-3 large-2")
    # print(f"Found {len(drinks_raw)} drinks.")
    drinks = []
    for drink in drinks_raw:
        name, url, ingredients_raw = get_drink_peliminary_info(drink)
        # print(f'Found drink: \n{name}\n{url}\n{ingredients_raw}')
        # quit(42)
        drinks.append([name, url, ingredients_raw])
    return drinks


def run_scrape():
    drinks = []
    try:  # Iterate through each page of recipes and scrape recipe elements
        page_num, max_pages = 0, 259
        tqdm.write(f"Scraping {max_pages} pages of drinks.")
        pbar = tqdm(total=max_pages, position=0, leave=True)
        while True:
            page_num += 1
            url = f"https://www.diffordsguide.com/cocktails/search?s=1&isrc=browse&ificm=1&ifipp=1&g%5Bdg%5D=1&gid=all&na=1&p={page_num}"
            page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(page.content, "html.parser")

            results = soup.find(id="content-container")
            drinks.extend(get_drinks(results))
            time.sleep(get_wait_time())
            pbar.update(1)
    except:
        print(f"Scraped {page_num} pages.")
        print(f"Scraped {len(drinks)} drinks.")

    # Save the data
    pd.DataFrame(drinks, columns=["name", "url", "ingredients"]).to_csv("diffords_drinks.csv", index=False)


# ======================================================================
# MAIN FUNCTION

if __name__ == "__main__":
    run_scrape()
