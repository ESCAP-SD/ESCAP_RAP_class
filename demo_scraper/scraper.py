"""
   # TO DO
    - docstrings
    - exceptions for robustness
    - logging
"""

from bs4 import BeautifulSoup, Tag
import requests
import pandas as pd
from datetime import datetime

from demo_scraper.utils import *

# from scraper.error import Scraper_Error, Parsing_Scraper_Error, Cleaning_Scraper_Error

def get_categories(input_url: str):
    """
 
    """   
    # Send a GET request to the URL
    response = requests.get(input_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the categories
        categories = soup.find_all("a", class_ = "category-list-image")
        
        # Create list to store the data
        category_urls = []

        # Loop through the categories and extract the names
        for category in categories:
            url = category.get("href", "N/A")
            category_urls.append(url)
            
        print("category_urls list has been created")
    else:
        print("Failed to retrieve the webpage.")
    return category_urls


def get_last_page_num(soup: Tag):
    """
    
    """
    # Find the number of pages to be iterated through
    pagenum_tag = soup.find_all("span", class_ = "pagination-hide")
    if pagenum_tag == [] :
        lastpage_num = 0

    else : 
        lastpage = pagenum_tag[-1].text.strip()  
        lastpage_num = int(lastpage[2:])
    
    print(f"Number of pages is {lastpage_num}")

    return lastpage_num

def save_data(dataframe: pd.DataFrame, save_location):
    """
    
    """
    dataframe.to_csv("{save_location}demo_scrape_{timestamp}.csv".format(
        save_location = save_location,
        timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    ), index=True)


def run_scraper(starting_url: str, save_location: str):
    """
    main function that orchestrates the whole scrape
    
    """
    category_urls = get_categories(starting_url)

    # now run a loop across the list of categories (dresses, tops etc ) 

    # Lists to store the product data
    product_data = []

    for category_url in category_urls:
        # Base URL for the product category
        base_url = category_url 

        # Send a GET request to the URL
        response = requests.get(base_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            # Find the number of pages to be iterated through
            lastpage_num = get_last_page_num(soup)
            for page_num in range(0, lastpage_num):
                # Modify the URL to include the page number
                url = f"{base_url}/Page-{page_num}-SortingAttribute-SortBy-asc"
    
                # Send a GET request to the URL
                response = requests.get(url)
    
                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Find the product listings
                    products = soup.find_all("div", class_="product-tile")
                    # break
                    # Loop through the product listings and extract the data
                    for product in products:
                        individual_product_data = parse_product_info(product)
                        product_data.append(individual_product_data)

        else:
            print("Failed to retrieve the webpage.")
            # TO DO - add to log as we'd want to log if a specific category could not be scraped
        df = pd.DataFrame.from_records(individual_product_data)
        save_data(df)
    return None



if __name__ == "__main__":
    starting_url = "https://www.farmers.co.nz/women/fashion"
    save_location = "../data/raw/"
    # print(get_categories(starting_url))
    product_data = run_scraper(starting_url, save_location)