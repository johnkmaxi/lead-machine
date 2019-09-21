"""Crawler classes for scraping web data

"""

import configparser
from datetime import datetime
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
        """Generate xpath of soup element

        Parameters
        ----------
        element : bs4 text or node

        Returns
        -------
        xpath as string
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
    source :
    driver_path :
    options :
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
        # self.options.headless = True
        if html_file:
            with open(html_file, mode='r', encoding='utf8') as page:
                self.source_html = page.read()
        else:
            # TODO: add exception handling for HTTPResponse errors
            self.source_html = urlopen(self.source)
        self.source_soup = BeautifulSoup(self.source_html, features='lxml')
        # self.searches = self.collect_search_list()
        super(MlsCrawler, self).__init__()
        self.conn = self.make_connection(None)


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
        browser = webdriver.Firefox(options=self.options, executable_path=self.driver_path)
        browser.get(self.source)
        # tag_xpath = self.xpath_soup(tag)
        # browser.find_element_by_xpath(tag_xpath).click()
        # TODO: Use selenium wait methods to handle this without requiring time.sleep for headless
        #time.sleep(5)
        # javascript for showing Single Line view
        # TODO: find the javascript function by locating the Client Single Line within the fxn
        browser.execute_script("__doPostBack('_ctl0$m_rptViewList$ctl00$ctl00','')")
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, features='lxml')
        time.sleep(3)
        browser.close()
        return soup

    def scrape_table_columns(self, soup):
        """Scrapes Single Line view table

        Each td tag associated with a column in the table has its own class
        designation. Each column of data can be extracted by grabbing all the td tags
        of each class.
        td class="d5m6" Sent
        td class="d5m7" Change Type
        td class="d5m8" Status
        td class="d5m9" MSL Number
        td class="d5m10" Address
        td class="d5m11" Price
        td class="d5m13" Beds
        td class="d5m14" Full Baths
        td class="d5m15" Half Baths
        td class="d5m17" Age Desc
        td class="d5m18" Living Area
        td class="d5m19" Year Built

        Parameters
        ----------
        soup : bs4 object
            The html from the Single Line view of an MLS search

        Returns
        -------
        data : dict
            Data extracted from the single line table
        """
        sent = [self.format_date(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m6"})]
        change_type = [x.span.contents[0].rstrip().lstrip() for x in soup.findAll('td', {'class':"d5m7"})]
        mls_num = [int(x.a.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m8"})]
        # status = [x.span.contents for x in soup.findAll('td', {'class':"d5m9"})][0]
        address = [x.span.contents[0].rstrip().lstrip() for x in soup.findAll('td', {'class':"d5m10"})]
        price = [self.format_money(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m11"})]
        beds = [int(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m13"})]
        fullbath = [int(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m14"})]
        halfbath = [int(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m15"})]
        age_desc = [x.span.contents[0].rstrip().lstrip() for x in soup.findAll('td', {'class':"d5m17"})]
        sq_ft_lv = [self.format_sqft(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m18"})]
        year_built = [self.format_year(x.span.contents) for x in soup.findAll('td', {'class':"d5m19"})]
        data = {
            'sent': sent,
            'changetype': change_type,
            'mlsnum': mls_num,
            'address': address,
            'price': price,
            'beds': beds,
            'fullbath': fullbath,
            'halfbath': halfbath,
            'agedesc': age_desc,
            'sqft': sq_ft_lv,
            'built': year_built
        }
        return data

    @staticmethod
    def format_date(date_str):
        """str to datetime object"""
        return datetime.strptime(date_str, '%m/%d/%Y')

    @staticmethod
    def format_money(money_str):
        """Removes $ and , from money_str"""
        return int(money_str.replace('$','').replace(',',''))

    @staticmethod
    def format_sqft(sqft_str):
        """Removes , from sqft_str"""
        return int(sqft_str.replace(',',''))

    @staticmethod
    def format_year(year_list):
        """Return an int of the year_str

        Year built values can return an empty list when scraping the MLS search.
        Only apply formatting if a value is present.
        """
        if len(year_list) == 1:
            year_str = year_list[0]
            if len(year_str) > 0:
                return int(year_str)
        else:
            return None

    def scrape_table_header(self, soup):
        """

        """
        columns = []
        for tdtag in soup.findAll('td'):
            try:
                columns.append(tdtag['data-mlheader'][3:])
            except:
                pass
        return [x for x in columns if len(x) > 0][1:]

    def save_html(self, soup, fname='html.html'):
        """Save html from bs4 object
        Parameters
        ----------

        """
        with open(fname, mode='w', encoding='utf') as p:
            p.write(str(soup.prettify()))
