"""
Move code from the notebook into a script
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime # need this new module

# Define the URL of the website
url = "https://www.farmers.co.nz/women/fashion"

# Send a GET request to the URL
response = requests.get(url)

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

# now run a loop across the list of categories (dresses, tops etc ) 

# Lists to store the product data
product_names = []
product_prices = []
product_urls = [] # get the full url for now can transform at later stage
product_category_urls = []
scrape_times = [] 
    
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
        pagenum_tag = soup.find_all("span", class_ = "pagination-hide")
        if pagenum_tag == [] :
            lastpage_num = 0
        
        else : 

            lastpage = pagenum_tag[-1].text.strip()  
            lastpage_num = int(lastpage[2:])

        print(f"Number of pages is {lastpage_num}")
    else:
        print("Failed to retrieve the webpage.")    

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
                name_tag = product.find("span", class_="product-title-span")
                price_tag = product.find("div", class_="current-price")
            
                # Extract and clean the product name
                name = name_tag.text.strip() if name_tag else "N/A"
            
                # Extract and clean the product price
                price = price_tag.text.strip() if price_tag else "N/A"

                # get time of scrape
                scrape_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            
                # get the product_url so that we can expand it later if needed
                product_url = product.find("a", href=True)["href"]

                # Append the data to the lists
                product_names.append(name)
                product_prices.append(price)
                product_urls.append(product_url) 
                product_category_urls.append(base_url)
                scrape_times.append(scrape_time)
                # Note - this is missing a few other things we require, hence we can expand this a bit
                # in the RAPifed version
        else:
            print(f"Failed to retrieve page {page_num}")

        # Create a DataFrame from the lists
    df = pd.DataFrame({
        "Product Name": product_names,
        "Product Price": product_prices,
        "Category Url" : product_category_urls,
        "Product Url" : product_urls,
        "Scrape Time" : scrape_times
    })

    # Save the DataFrame to a CSV file
    df.to_csv("../data/raw/farmers_womens_fashion.csv", index=False)

    print(f"Data has been written to farmers_womens_fashion.csv for page {category_url}")