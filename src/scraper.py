"""Crawler classes for scraping web data

"""

import configparser
from datetime import datetime
import itertools
import random
import time
import urllib.request

from bs4 import BeautifulSoup
from lxml.html import fromstring
import psycopg2
import requests
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
        driver_path="C:/Users/John Maxi/geckodriver.exe",
        driver_options=None
    ):
        self.source = source
        self.driver_path = driver_path
        self.date = datetime.now().date()
        self.options = Options()
        #self.options.headless = True
        if html_file:
            with open(html_file, mode='r', encoding='utf8') as page:
                self.source_html = page.read()
            self.source_soup = BeautifulSoup(self.source_html, features='lxml')
        super(MlsCrawler, self).__init__()
        self.conn = self.make_connection(None)

    def get_source(self):
        """Make request to source URL and return page HTML"""
        proxy = self.get_proxies()
        user_agent = self.get_user_agent()
        req = urllib.request.Request(self.source, headers={'User-Agent':user_agent})
        req.set_proxy(proxy, 'https')
        source_html =  urllib.request.urlopen(req)
        return source_html

    # def collect_search_list(self):
    #     """Returns a list of links containing search results
    #
    #     Returns
    #     -------
    #     searches : list
    #
    #     deprecated using individual search links as the sources
    #     """
    #     links = self.source_soup.findAll('a', id=lambda x: x and 'ucItemView_m_lnkSubject' in x)
        return links

    def single_line_view(self):
        """Changes the page view to Single Line

        Single Line view is created by a JavaScript-type link. Use selenium to
        process the link.

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
        browser = webdriver.Firefox(options=self.options, executable_path=self.driver_path, service_log_path=None)
        browser.get(self.source)
        # tag_xpath = self.xpath_soup(tag)
        # browser.find_element_by_xpath(tag_xpath).click()
        # TODO: Use selenium wait methods to handle this without requiring time.sleep for headless
        #time.sleep(5)
        # javascript for showing Single Line view
        # TODO: find the javascript function by locating the Client Single Line within the fxn
        browser.execute_script("__doPostBack('_ctl0$m_rptViewList$ctl00$ctl00','')")
        time.sleep(random.randint(11,16))
        try:
            _ = browser.find_element_by_link_text("See More Results")
            print(_)
            browser.execute_script("PortalResultsJs.getNextDisplaySet();")
            time.sleep(random.randint(11,16))
        except:
            pass
        soup = BeautifulSoup(browser.page_source, features='lxml')
        time.sleep(random.randint(11,16))
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
        beds = [self.format_result_list(x.span.contents) for x in soup.findAll('td', {'class':"d5m13"})]
        fullbath = [self.format_result_list(x.span.contents) for x in soup.findAll('td', {'class':"d5m14"})]
        halfbath = [self.format_result_list(x.span.contents) for x in soup.findAll('td', {'class':"d5m15"})]
        age_desc = [x.span.contents[0].rstrip().lstrip() for x in soup.findAll('td', {'class':"d5m17"})]
        sq_ft_lv = [self.format_sqft(x.span.contents[0].rstrip().lstrip()) for x in soup.findAll('td', {'class':"d5m18"})]
        year_built = [self.format_result_list(x.span.contents) for x in soup.findAll('td', {'class':"d5m19"})]
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

    def get_listing_info(self, link_txt, properties=None):
        """Parse information from individual listing page

        Parameters
        ----------
        link_txt : str
            Indicates a row in an HTML table. The value matching `link_txt` is clicked
        properties : list of str
            If not None, only keys that are in properties are included in info.
            Otherwise, return all items from info.

        Returns
        -------
        info : dict
        """
        browser = webdriver.Firefox(options=self.options, executable_path=self.driver_path, service_log_path=None)
        browser.get(self.source)
        browser.execute_script("__doPostBack('_ctl0$m_rptViewList$ctl00$ctl00','')")
        time.sleep(random.randint(11,16))
        try:
            _ = browser.find_element_by_link_text("See More Results")
            print(_)
            browser.execute_script("PortalResultsJs.getNextDisplaySet();")
            time.sleep(random.randint(11,16))
        except:
            pass
        # find link using link_txt
        link = browser.find_element_by_link_text(link_txt)
        # extract the href from the element and get just the javascript fxn to execute
        browser.execute_script(link.get_attribute('href')[len('javascript:'):])
        #link.click(on_element=link)
        time.sleep(random.randint(11,16))
        soup = BeautifulSoup(browser.page_source, features='lxml')
        info = self.parse_listing_info(soup, properties=properties)
        time.sleep(random.randint(2,5))
        browser.close()
        return info


    def parse_listing_info(self, soup, properties=None):
        """
        Scrapes the information contained in the tables in the listing.

        If values passed in properties are not in info, then the value None is
        returned for that key.

        Parameters
        ----------
        soup : bs4 object
        properties : list of str
            A subset of keys from info to be returned

        Returns
        -------
        info : dict
            Property Type, Dwelling Type, Zip, Lp/SqFt, Neighborhood, DOM
            City, Zip, Bound Streets, Lot Size, Lot Description, Acres#, Age
        """
        values = [x.text for x in soup.select('.col-xs-7')]
        keys = [x.text for x in soup.select('.col-xs-5')]
        keys = keys[-len(values):]
        info = dict(zip(keys,values))
        if properties is None: # return all info items
            return info
        return {k: info.get(k, None) for k in properties}

    @staticmethod
    def format_date(date_str):
        """str to datetime object"""
        return datetime.strptime(date_str, '%m/%d/%Y')

    @staticmethod
    def format_money(money_str):
        """Removes $ and , from money_str"""
        return int(float(money_str.replace('$','').replace(',','')))

    @staticmethod
    def format_sqft(sqft_str):
        """Removes , from sqft_str"""
        return int(sqft_str.replace(',',''))

    @staticmethod
    def make_int(string):
        """Try to make an int, otherwise make None"""
        try:
            return int(string)
        except:
            return None

    @staticmethod
    def format_result_list(result_list):
        """Return an int the passed ['str']

        Some values in the table can be empty.

        Parameters
        ----------
        result_list : list of str
            Should have either 1 or 0 items in the list

        Returns
        -------
        int
        """
        if len(result_list) == 1:
            result_str = result_list[0]
            if len(result_str) > 0:
                #print(result_list, result_str.rstrip().lstrip())
                return int(result_str.rstrip().lstrip())
        else:
            return None

    @staticmethod
    def get_proxies():
        """Get a random proxy for spoofing"""
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr'):
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                #Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return random.choice(list(proxies))

    @staticmethod
    def get_user_agent():
        """Get a random user agent from a specified list"""
        user_agent_list = [
            #Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        return random.choice(user_agent_list)

    # def scrape_table_header(self, soup):
    #     """Get the table headers of the single line view
    #
    #     """
    #     columns = []
    #     for tdtag in soup.findAll('td'):
    #         try:
    #             columns.append(tdtag['data-mlheader'][3:])
    #         except:
    #             pass
    #     return [x for x in columns if len(x) > 0][1:]

    def save_html(self, soup, fname='html.html'):
        """Save html from bs4 object
        Parameters
        ----------

        """
        with open(fname, mode='w', encoding='utf') as p:
            p.write(str(soup.prettify()))
