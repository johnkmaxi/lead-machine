"""Crawler classes for scraping web data

"""

import configparser
from urllib.request import urlopen

from bs4 import BeautifulSoup
import psycopg2

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
    conn : psycopg2 connection object

    Methods
    -------
    make_connection(conn_info)
    to_db(query)

    """
    def __init__(self, source=None, conn_info=None):
        self.conn = self.make_connection(conn_info)
        self.conn.set_session(autocommit=True)

    def make_connection(self, conn_info, db='POSTGRES'):
        """Returns a connection to database

        Parameters
        ----------
        conn_info : str
            A filepath to a config file with database connection information

        Returns
        -------
        conn : psycopg2 connection object
        """
        if conn_info is None: # use default db on local host
            conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
        else: # parse the config file and connect
            config = configparser.ConfigParser()
            config.read(conn_info)
            host = config[db]['host']
            #port = int(config[db]['port'])
            #service_name = config[db]['service_name']
            dbname = config[db]['dbname']
            username = config[db]['username']
            password = config[db]['password']
            conn = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
        return conn

    def to_db(self, query, params=None):
        """Writes a query to a database

        Parameters
        ----------
        query : str
        """
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur

class MlsCrawler(BaseCrawler):
    """A crawler for parsing the MLS portal

    Parameters
    ----------
    source : str
        A URL indicating the where the crawler should begin data collection

    Attributes
    ----------
    searches : list
        The links to individual searches available from the My Searches page

    Methods
    -------
    collect_search_list(), collects the links on the my searches page
    click(url), follows the passed URL link
    nav_single_line_view(), navigates to the single line client view
    home(), returns to the `source` URL
    collect(), parses HTML table of listings
    http_error_handling(), build in seperate function or within each fxn
    attribute_error_handling(), if an HTML attribute does not exist


    """
    def __init__(self, source):
        self.source = source
        self.searches = self.collect_search_list()

    def collect_search_list(self):
        """Returns a list of links containing search results

        Returns
        -------
        searches : list

        """
        html = urlopen(self.source)
        soup = BeautifulSoup(html)
        links = soup.findAll('a', id=lambda x: x and 'ucItemView_m_lnkSubject' in x)
        return links
