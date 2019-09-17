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

    Attributes
    ----------


    Methods
    -------
    make_connection(conn_info)
    to_db(query)

    """
    def __init__(self, source=None, conn_info=None):
        pass

    @staticmethod
    def click(url):
        """Opens the passed URL

        Parameters
        ----------
        url : str
            A URL link to open

        Returns
        -------
        response : HTTPResponse object
        """


class MlsCrawler(BaseCrawler):
    """A crawler for parsing the MLS portal

    Parameters
    ----------
    source : str
        A URL indicating the where the crawler should begin data collection
    html_file : str, default None
        A filename to use as the html source. If used, the source URL is not
        used.

    Attributes
    ----------
    source_html : HTTPResponse object
        The html of the source URL
    source_soup : BeautifulSoup object
        Parsed HTML of source URL
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
    def __init__(self, source, html_file=None):
        self.source = source
        if html_file:
            with open(html_file, mode='r', encoding='utf8') as page:
                self.source_html = page.read()
        else:
            self.source_html = urlopen(self.source)
        self.source_soup = BeautifulSoup(self.source_html)
        self.searches = self.collect_search_list()


    def collect_search_list(self):
        """Returns a list of links containing search results

        Returns
        -------
        searches : list

        """
        links = self.source_soup.findAll('a', id=lambda x: x and 'ucItemView_m_lnkSubject' in x)
        return links
