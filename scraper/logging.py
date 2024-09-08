class pysqlcError(Exception):
    """
    The main exception handler for pysql
    """

    def __init__(self, reason):
        Exception.__init__(self, reason)


class ScrapeError(pysqlcError):
    """
    Error when scraping and we get unintended requirements
    """
    pass