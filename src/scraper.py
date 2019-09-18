"""Crawler classes for scraping web data

"""

import configparser
import itertools
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from db import BaseDb

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
    click(url), opens the URL

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
        pass

    @staticmethod
    def xpath_soup(element):
        """
        Generate xpath of soup element
        :param element: bs4 text or node
        :return: xpath as string
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            previous = itertools.islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

class MlsCrawler(BaseCrawler, BaseDb):
    """A crawler for parsing the MLS portal

    Parameters
    ----------
    source : str
        A URL indicating the where the crawler should begin data collection
    html_file : str, default None
        A filename to use as the html source. If used, the source URL is not
        used.
    driver_path : str
        File location of gecko webdriver for selenium
    driver_options: str
        Options to use when initializing selenium. Default is None. Driver is
        executed in the headless state.

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

    nav_single_line_view(), navigates to the single line client view
    home(), returns to the `source` URL
    collect(), parses HTML table of listings
    http_error_handling(), build in seperate function or within each fxn
    attribute_error_handling(), if an HTML attribute does not exist


    """
    def __init__(self,
        source,
        html_file=None,
        driver_path="C:\\Users\\John Maxi\\Box\\MaxiHoldings\\lead-machine\\geckodriver.exe",
        driver_options=None
    ):
        self.source = source
        self.driver_path = driver_path
        self.options = Options()
        #self.options.headless = True
        if html_file:
            with open(html_file, mode='r', encoding='utf8') as page:
                self.source_html = page.read()
        else:
            # TODO: add exception handling for HTTPResponse errors
            self.source_html = urlopen(self.source)
        self.source_soup = BeautifulSoup(self.source_html)
        self.searches = self.collect_search_list()
        super(MlsCrawler, self).__init__()


    def collect_search_list(self):
        """Returns a list of links containing search results

        Returns
        -------
        searches : list

        """
        links = self.source_soup.findAll('a', id=lambda x: x and 'ucItemView_m_lnkSubject' in x)
        return links

    def single_line_view(self, tag):
        """Changes the page view to Single Line

        Single Line view is created by a JavaScript-type link. Use selenium to
        process the link.

        Parameters
        ----------
        tag : bs4.element.Tag

        Return
        ------
        soup : BeautifulSoup object
            The link associated with tag is followed and the parsed html is returned

        Notes
        -----
        The single line view of the results page is displayed by a executing
        JavaScript. The code used here comes from inspecting the element and
        finding this tag:
        <a
            onclick="PortalResultsJs.displayChanged('more');"
            href="javascript:__doPostBack('_ctl0$m_rptViewList$ctl00$ctl00','')"
        >
            Client Single Line
        </a>

        The javascript function is hardcoded into the function.

        """
        browser = webdriver.Firefox(firefox_options=self.options, executable_path=self.driver_path)
        browser.get(self.source)
        tag_xpath = self.xpath_soup(tag)
        browser.find_element_by_xpath(tag_xpath).click()
        # TODO: Use selenium wait methods to handle this without requiring time.sleep for headless
        #time.sleep(5)
        # javascript for showing Single Line view
        # TODO: find the javascript function by locating the Client Single Line within the fxn
        browser.execute_script("__doPostBack('_ctl0$m_rptViewList$ctl00$ctl00','')")
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source)
        browser.close()
        return soup

    def scrape_table(self):
        """Scrapes Single Line view table

        """
        pass

    def save_html(self, soup, fname='html.html'):
        """
        """
        with open(fname, mode='w', encoding='utf') as p:
            p.write(str(soup.prettify())
