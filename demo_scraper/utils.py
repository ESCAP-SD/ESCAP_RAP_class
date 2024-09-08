from bs4 import BeautifulSoup, Tag
from demo_scraper.error import Parsing_Scraper_Error, Cleaning_Scraper_Error


def parse_product_name(soup: Tag):
    """
    
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    try:
        name_tag = soup.find("span", class_="product-title-span")
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to parse product name:",str(e))
    return name_tag


def parse_price(soup: Tag):
    """
    
    """
    try:
        price = soup.find("div", class_="current-price")
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to parse price:",str(e))
    return price


def parse_product_url(soup: Tag):
    """
    #TO DO: convert to logging - as this one is less critical
    """
    if not type(soup) == Tag:
        raise TypeError("Invalid input")
    try:
        product_url = product.find("a", href=True)["href"]
    except Exception as e:
        raise Parsing_Scraper_Error("Failed to parse individual product URL:",str(e))
    return product_url

def clean_name_tag(name_tag: Tag):
    """
    
    """
    if not type(name_tag) == Tag:
        raise TypeError("Invalid input")
    try:
        name = name_tag.text.strip() if name_tag else "N/A"
    except Exception as e:
        raise Cleaning_Scraper_Error("Failed to clean name_tag:",str(e))
    return name


def clean_price_tag(price_tag: Tag):
    """
    
    """
    if not type(price_tag) == Tag:
        raise TypeError("Invalid input")
    try:
        price = price_tag.text.strip() if price_tag else "N/A"
    except Exception as e:
        raise Cleaning_Scraper_Error("Failed to clean price tag:",str(e))
    return price


def parse_product_info(soup: Tag):
    """
    
    """
    #parse out and clean product name
    name_tag = parse_product_name(soup)
    name = clean_name_tag(name_tag)

    #parse out and clean price for the product
    price_tag = parse_price(soup)
    price = clean_price_tag(price_tag)

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


