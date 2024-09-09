class Scraper_Error(Exception):
    """
    The main exception
    """

    def __init__(self, reason):
        Exception.__init__(self, reason)

class Parsing_Scraper_Error(Scraper_Error):
    """
    Error when parsing BeutifulSoup objects or related
    """
    pass

class Cleaning_Scraper_Error(Scraper_Error):
    """
    Error cleaning strings or related
    """
    pass

class Save_Scraper_Error(Scraper_Error):
    """
    Error saving
    """
    pass