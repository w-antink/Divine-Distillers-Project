#Import necessary packages=============================================
import psycopg2 # type: ignore
import selenium # type: ignore
import re #Necessary for the conv_names function
import time
import json
from selenium import webdriver  
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
#======================================================================

#======================================================================
#SCRAPER SUB-FUNCTIONS

def find_cocktails(driver): #Find and store all cocktail recipes on page
    try:
        #Locate all cocktail recipe elements
        recipe_elements = driver.find_elements(By.CLASS_NAME, 'cell small-6 medium-3 large-2')

        if recipe_elements:
            for i, recipe_element in enumerate(recipe_elements):
                pass #Finish
    except:
        pass #Finish

#======================================================================

#======================================================================
#SCRAPER OPERATION

#Initialize webdriver
    options = Options()
    options.headless = False  # don't trust the user to not mess with the slides
    driver = webdriver.Firefox()

    if True:
        driver.get("https://www.diffordsguide.com/cocktails/search?s=1&isrc=browse&ificm=1&ifipp=1&g%5Bdg%5D=1&a=35&na=1&cal=425&gid=all")
