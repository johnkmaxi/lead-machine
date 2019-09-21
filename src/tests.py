"""Tests

"""

import unittest

import bs4
import datetime

# import pandas as pd

from db import BaseDb
from scraper import BaseCrawler
from scraper import MlsCrawler
from create_tables import create_database
from create_tables import delete_database
from create_tables import create_tables
from create_tables import drop_tables
from sources import MLS_SEARCHES
from sources import MF_7TH_9TH_MARIGNY_BYWATER
from sources import SF_7TH_9TH_MARIGNY_BYWATER
from sources import MF_70114_70131
from sources import SF_70114_70131
from sources import MF_70119_70122_70124
from sources import SF_70119_70122_70124
from sources import MF_70118_70125_70113_70130_70115
from sources import SF_70118_70125_70113_70130_70115
from sources import SF_FQ
from sql_queries import leads_insert

# class TestDb(unittest.TestCase):
#     """
#
#     """
#
#     @classmethod
#     def setUpClass(cls):
#         """Create the testing database
#         """
#         create_database('config.cfg', schema='testleadmachine')
#         cls.test_crawler = BaseDb()
#         create_tables(cls.test_crawler.conn)
#
#     @classmethod
#     def tearDownClass(cls):
#         """Delete the testing database
#         """
#         drop_tables(cls.test_crawler.conn)
#         delete_database(cls.test_crawler.conn, schema='testleadmachine')
#         cls.test_crawler.conn.close()
#
#     def test_no_config(self):
#         base_crawler = BaseDb()
#         self.assertTrue(True)
#
#     def test_config(self):
#         base_crawler = BaseDb(conn_info='config.cfg')
#         self.assertTrue(True)
#
#     def test_config_fail(self):
#         try:
#             base_crawler = BaseDb(conn_info='notmyconfig.cfg')
#         except KeyError:
#             self.assertTrue(True)
#
#     def test_base_crawler_to_db(self):
#         self.test_crawler.to_db(leads_insert, params=[datetime.datetime(2019,1,1),'varchar',1,'varchar',1,1,1,1,'varchar',1,1])
#         cur = self.test_crawler.to_db('select * from leads')
#         results = cur.fetchall()
#         self.assertEqual(1, len(results))
#
#
# class TestMlsScraper(unittest.TestCase):
#     """MLS scraping tests
#
#     """
#
#     @classmethod
#     def setUpClass(cls):
#         """Create the testing database
#         """
#         cls.crawler = MlsCrawler(MLS_SEARCHES, html_file='mls_source_html_test.html')
#         cls.crawler.searches = cls.crawler.collect_search_list()
#         with open('singlelineview.html', mode='r', encoding='utf8') as p:
#             cls.single_line_soup = bs4.BeautifulSoup(p.read(), features='lxml')
#         create_database('config.cfg', schema='testleadmachine')
#         create_tables(cls.crawler.conn)
#
#     @classmethod
#     def tearDownClass(cls):
#         drop_tables(cls.crawler.conn)
#         delete_database(cls.crawler.conn, schema='testleadmachine')
#         cls.crawler.conn.close()
#
#     def test_read_from_file(self):
#         self.assertIs(type(self.crawler.source_html), str)
#
#     def test_collect_search_list_len(self):
#         self.assertEqual(9, len(self.crawler.searches))
#
#     def test_collect_search_list_names(self):
#         link_text = [x.text.strip() for x in self.crawler.searches]
#         self.assertTrue("Single family: FQ & Iberville" in link_text)
#         self.assertTrue("Multi-family: 7& 9th wards, Marigny/Bywater" in link_text)
#         self.assertTrue("Single family: 7th & 9th wards, Marigy/Bywater" in link_text)
#         self.assertTrue("Multi-family: 70114, 70131" in link_text)
#         self.assertTrue("Single family: 70114, 70131" in link_text)
#         self.assertTrue("Multi-family: 70119, 70122, 70124" in link_text)
#         self.assertTrue("Single family: 70119, 70122, 70124" in link_text)
#         self.assertTrue("Multi-family: 70118 70125 70113 70130 70115" in link_text)
#         self.assertTrue("Single family: 70118 70125 70113 70130 70115" in link_text)
#
#     def test_link_type(self):
#         # print(type(self.crawler.searches[0]))
#         # print(self.crawler.searches[0])
#         # print(self.crawler.searches[0].attrs["href"])
#         pass
#
#     def test_single_line_view(self):
#         self.single_line_soup = self.crawler.single_line_view(self.crawler.searches[0])
#         self.assertIs(type(self.single_line_soup), bs4.BeautifulSoup)
#
#     def test_scrape_table_header(self):
#         columns = self.crawler.scrape_table_header(self.single_line_soup)
#         expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
#         self.assertTrue(columns == expected)
#
#     def test_scrape_table_data(self):
#         data = self.crawler.scrape_table_columns(self.single_line_soup)
#         # for i in range(len(data)):
#         #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
#         #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
#         #print(df.head())
#         self.assertTrue(len(data) > 0)
#
#     def test_write_to_db(self):
#         data = self.crawler.scrape_table_columns(self.single_line_soup)
#         cur = self.crawler.to_db(
#             leads_insert,
#             params=(data['sent'][0],
#                     data['changetype'][0],
#                     data['mlsnum'][0],
#                     data['address'][0],
#                     data['price'][0],
#                     data['beds'][0],
#                     data['fullbath'][0],
#                     data['halfbath'][0],
#                     data['agedesc'][0],
#                     data['sqft'][0],
#                     data['built'][0])
#         )
#         cur.execute('select * from leads')
#         results = cur.fetchall()
#         self.assertEqual(1, len(results))

class TestMlsScraperFQ(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_FQ)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_7TH_9TH_MARIGNY_BYWATER)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(MF_7TH_9TH_MARIGNY_BYWATER)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(MF_70114_70131)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_70114_70131)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(MF_70119_70122_70124)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_70119_70122_70124)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(MF_70118_70125_70113_70130_70115)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_70118_70125_70113_70130_70115)
        cls.soup = cls.crawler.single_line_view(None)
        create_database('config.cfg', schema='testleadmachine')
        create_tables(cls.crawler.conn)

    @classmethod
    def tearDownClass(cls):
        drop_tables(cls.crawler.conn)
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    def test_scrape_table_header(self):
        columns = self.crawler.scrape_table_header(self.soup)
        expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
        self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        # for i in range(len(data)):
        #     print(data['sent'][i],data['changetype'][i],data['mlsnum'][i])
        #df = pd.DataFrame(data, index=['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']).T
        #print(df.head())
        self.assertTrue(len(data) > 0)

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        cur = self.crawler.to_db(
            leads_insert,
            params=(data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0])
        )
        cur.execute('select * from leads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

if __name__ == '__main__':
    unittest.main()
