"""
   # TO DO
    - doc strings
    - exceptions for robustness
    - logging
"""

from bs4 import BeautifulSoup, Tag
import requests
import pandas as pd
# from datetime import datetime

from utils import *
# from demo_scraper.error import Scraper_Error, Parsing_Scraper_Error, Cleaning_Scraper_Error


def run_scraper(starting_url: str, save_location: str):
    """
    main function that orchestrates the whole scrape
    
    """
    # Create an empty array to store data we scrape. As its not size delimited,
    # it can be extended as we need later on
    product_data = []

    category_urls = get_and_parse_categories(starting_url)

    # now run a loop across the list of categories (dresses, tops etc ) 
    for category_url in category_urls:

        # GET the data for the first page of the category
        category_page1_soup = get_site_data(category_url)

        # Save all the products on this first page
        product_data = parse_products_on_page(category_page1_soup, product_data)

        # As there is likely more than 1 page, find out how many more pages this
        # category has to go through and if so, go through these pages
        lastpage_num = parse_last_page_num(category_page1_soup)
        if lastpage_num > 0:
            #Iterate through each page 
            for page_num in range(1, lastpage_num):
                # Modify the GET URL to include the page number
                url = f"{category_url}/Page-{page_num}-SortingAttribute-SortBy-asc"
    
                # GET this page
                next_page_soup = get_site_data(url)

                # Parse and save all the products on this page
                product_data = parse_products_on_page(next_page_soup, product_data)

        save_data(product_data, save_location)
        
    return None


if __name__ == "__main__":
    starting_url = "https://www.farmers.co.nz/women/fashion"
    save_location = "../data/raw/"
    # print(get_categories(starting_url))
    product_data = run_scraper(starting_url, save_location)