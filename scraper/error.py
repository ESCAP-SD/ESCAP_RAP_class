class Scraper_Error(Exception):
    """
    The main exception handler for pysql
    """

    def __init__(self, reason):
        Exception.__init__(self, reason)


class Parsing_Scraper_Error(ScrapeError):
    """
    Error when scraping and we get unintended requirements
    """
    pass

class Cleaning_Scraper_Error(pysqlcError):
    """
    Error when scraping and we get unintended requirements
    """
    pass