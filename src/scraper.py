"""Crawler for scraping web data

"""

class BaseCrawler:
    """Collects information from web-based sources and stores to database

    Parameters
    ----------
    source : str
        A URL indicating the where the crawler should begin data collection
    conn_info : str
        A filepath to a config file with database connection information

    Attributes
    ----------
    conn :
        Database connection object

    Methods
    -------
    make_connection(conn_info)
    to_db(query)
    """
