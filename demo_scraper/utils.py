from bs4 import BeautifulSoup, Tag
import requests
import pandas as pd
from error import *
from datetime import datetime

def get_site_data(input_url:str):
    """
    
    """
    if not type(input_url) == str:
        raise TypeError("Invalid input")
    # Send a GET request to the URL
    response = requests.get(input_url)
    # TO DO: add to log to record every call we made to the site and when

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
    else:
        raise Scraper_Error("Did not get a 200 response, could not get or scrape page")
    return soup


def get_and_parse_categories(input_url: str):
    """
    
    """
    if not type(input_url) == str:
        raise TypeError("Invalid input")
    # Get the data
    soup = get_site_data(input_url)
        
    # Find the categories
    categories = soup.find_all("a", class_ = "category-list-image")
        
    # Create list to store the data
    category_urls = []

    # Loop through the categories and extract the names
    for category in categories:
        url = category.get("href", "N/A")
        category_urls.append(url)
            
    print("category_urls list has been created")
    return category_urls

def parse_product_name(soup: Tag):
    """
    
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    try:
        name_tag = soup.find("span", class_="product-title-span")
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to parse product name:",str(e))
    try:
        name = name_tag.text.strip() if name_tag else "N/A"
    except Exception as e:
        raise Cleaning_Scraper_Error("Failed to clean name_tag:",str(e))    

    return name


def parse_price(soup: Tag):
    """
    
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    try:
        price_tag = soup.find("div", class_="current-price")
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to parse price:",str(e))
    try:
        price = price_tag.text.strip() if price_tag else "N/A"
    except Exception as e:
        raise Cleaning_Scraper_Error("Failed to clean price tag:",str(e))    
    return price


def parse_product_url(soup: Tag):
    """
    #TO DO: convert raise to logging - as this one is less critical
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    try:
        product_url = soup.find("a", href=True)["href"]
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to parse individual product URL:",str(e))
    return product_url

def parse_last_page_num(soup: Tag):
    """
    
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    # Find the number of pages to be iterated through
    pagenum_tag = soup.find_all("span", class_ = "pagination-hide")
    # If we return no other pages, then return 0 as this will mean the main page loop will run once
    if pagenum_tag == [] :
        lastpage_num = 0

    else : 
        # Clean the tag to return the real project name
        lastpage = pagenum_tag[-1].text.strip()  
        lastpage_num = int(lastpage[2:])
    
    print(f"Number of pages is {lastpage_num}")

    return lastpage_num


def parse_products_on_page(soup: Tag, product_data: list):
    """
    
    """
    if not type(soup) == Tag and not type(product_data) == list:
        raise TypeError("Invalid input")
    try:
        # Get the products on the page
        products = soup.find_all("div", class_="product-tile")
        # Loop through all products and parse them all
        for product in products:
            individual_product_data = parse_product_info(product)
            product_data.append(individual_product_data)
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to separate out products on page",str(e))
    return products


# -----first order functions------------


def parse_product_info(soup: Tag):
    """
    NOTE: this is highly extensible without any downstream dependencies for the format of the 
    returned dictionary (as long as its consistent as its a dataframe)
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    #parse out and clean product name
    name = parse_product_name(soup)

    #parse out and clean price for the product
    price = parse_price(soup)

    # log the time the file was being processed to get the scrape_time
    scrape_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # get the product_url so that we can expand the data we get later if needed
    product_url = parse_product_url(soup)

    return {
        "product_name":name,
        "price":price,
        "scrape_time":scrape_time,
        "product_url":product_url
    }


def save_data(product_data: list, save_location: str, save_locally=True):
    """
    
    """
    if not type(product_data) == list and not save_location == str and not type(save_locally) == bool:
        raise TypeError("Invalid input")
    df = pd.DataFrame.from_records(product_data)
    try:
        #try to save in the specified location
        df.to_csv("{save_location}demo_scrape_{timestamp}.csv".format(
            save_location = save_location,
            timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        ), index=True)
    except Exception as e:
        #if that does not work, save locally (wherever this file is run)
        if save_locally == True:
            df.to_csv("demo_scrape_{timestamp}.csv".format(
                save_location = save_location,
                timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            ), index=True)
        else:
            raise     
