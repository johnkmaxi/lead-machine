"""Tests

"""

import unittest

import bs4
import datetime
import requests

# import pandas as pd

from db import BaseDb
from scraper import BaseCrawler
from scraper import MlsCrawler
from create_tables import create_connection
from create_tables import create_database
from create_tables import delete_database
from create_tables import create_table
from create_tables import drop_table
from sources import MLS_SEARCHES
from sources import MF_7TH_9TH_MARIGNY_BYWATER
from sources import SF_7TH_9TH_MARIGNY_BYWATER
from sources import SF_70119_70122_70124
from sources import MF_70118_70125_70113_70130_70115
from sources import SF_70118_70125_70113_70130_70115
from sources import SF_FQ
from sql_queries import testtables
from sql_queries import testcolumns

INSERT = ("""
INSERT INTO TESTLEADS(SCRAPE_DATE, APPEARED_DATE, CHANGE_TYPE, MLS_NUM, ADDRESS, CURRENT_PRICE, BEDS, FULL_BATHS, HALF_BATHS, AGE_DESC, YR_BLT, SQ_FEET_LV,
                  PROPERTY_TYPE, DWELLING_TYPE, CITY, ZIP, LP_SQ_FT, NEIGHBORHOOD, DOM, BOUNDING_STREETS, LOT_SIZE, LOT_DESCRIPTION, ACRES, AGE)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (APPEARED_DATE, ADDRESS)
DO UPDATE SET (SCRAPE_DATE, CHANGE_TYPE, MLS_NUM, CURRENT_PRICE
,BEDS ,FULL_BATHS, HALF_BATHS, AGE_DESC, YR_BLT, SQ_FEET_LV,
PROPERTY_TYPE, DWELLING_TYPE, CITY, ZIP, LP_SQ_FT, NEIGHBORHOOD, DOM, BOUNDING_STREETS, LOT_SIZE, LOT_DESCRIPTION, ACRES, AGE) = (EXCLUDED.SCRAPE_DATE, EXCLUDED.CHANGE_TYPE, EXCLUDED.MLS_NUM, EXCLUDED.CURRENT_PRICE
,EXCLUDED.BEDS ,EXCLUDED.FULL_BATHS, EXCLUDED.HALF_BATHS, EXCLUDED.AGE_DESC, EXCLUDED.YR_BLT, EXCLUDED.SQ_FEET_LV,
EXCLUDED.PROPERTY_TYPE, EXCLUDED.DWELLING_TYPE, EXCLUDED.CITY, EXCLUDED.ZIP, EXCLUDED.LP_SQ_FT, EXCLUDED.NEIGHBORHOOD, EXCLUDED.DOM, EXCLUDED.BOUNDING_STREETS, EXCLUDED.LOT_SIZE, EXCLUDED.LOT_DESCRIPTION, EXCLUDED.ACRES, EXCLUDED.AGE)
""")

# class TestDb(unittest.TestCase):
#     """
#
#     """
#
#     def setUp(self):
#         """Create the testing database
#         """
#         self.conn = create_connection('config.cfg')
#         create_database(self.conn, schema='testleadmachine')
#         self.test_crawler = BaseDb()
#         create_table(self.test_crawler.conn, 'TESTLEADS', testcolumns)
#
#     def tearDown(self):
#         """Delete the testing database
#         """
#         drop_table(self.test_crawler.conn, 'TESTLEADS')
#         delete_database(self.test_crawler.conn, schema='testleadmachine')
#         self.test_crawler.conn.close()
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
#         self.test_crawler.to_db(INSERT, params=[datetime.datetime(2019,1,1),datetime.datetime(2019,1,1),'varchar',1,'varchar',1,1,1,1,'varchar',1,1,'varchar',
#     'varchar',
#     'varchar',
#     1,
#     1,
#     'varchar',
#     1,
#     'varchar',
#     'varchar',
#     'varchar',
#     'varchar',
#     'varchar'])
#         cur = self.test_crawler.to_db('select * from testleads')
#         results = cur.fetchall()
#         self.assertEqual(1, len(results))
#
#     def test_update_on_conflict(self):
#         self.test_crawler.to_db(INSERT, params=[datetime.datetime(2019,1,1),datetime.datetime(2019,1,1),'varchar',1,'varchar',1,1,1,1,'varchar',1,1,'varchar',
#     'varchar',
#     'varchar',
#     1,
#     1,
#     'varchar',
#     1,
#     'varchar',
#     'varchar',
#     'varchar',
#     'varchar',
#     'varchar'])
#         self.test_crawler.to_db(INSERT, params=[datetime.datetime(2019,1,2),datetime.datetime(2019,1,1),'varchar',2,'varchar',1,2,2,2,'varchar',2,2,'varchar',
# 'varchar',
# 'varchar',
# 2,
# 2,
# 'varchar',
# 2,
# 'varchar',
# 'varchar',
# 'varchar',
# 'varchar',
# 'varchar'])
#         cur = self.test_crawler.to_db('select * from testleads')
#         results = cur.fetchall()
#         self.assertEqual(2, results[0][4])
#
# @unittest.skip('test is deprecated')
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
#         conn = create_connection('config.cfg')
#         create_database(conn, schema='testleadmachine')
#         create_table(cls.crawler.conn)
#
#     @classmethod
#     def tearDownClass(cls):
#         drop_table(cls.crawler.conn)
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
#         cur.execute('select * from testleads')
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
        cls.soup = cls.crawler.single_line_view()
        conn = create_connection('config.cfg')
        create_database(conn, schema='testleadmachine')
        create_table(cls.crawler.conn, 'TESTLEADS', testcolumns)

    @classmethod
    def tearDownClass(cls):
        drop_table(cls.crawler.conn, 'TESTLEADS')
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    # def test_scrape_table_header(self):
    #     columns = self.crawler.scrape_table_header(self.soup)
    #     expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
    #     print(columns)
    #     self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        self.assertTrue(len(data) > 0)

    def test_scrape_listing_info(self):
        data = self.crawler.get_listing_info('2195474', properties=['List Price','MLS Number','Zip'])
        self.assertEqual(3, len(data))
    @unittest.skip('skip')
    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        listing_data = self.crawler.get_listing_info('2195474', properties=['Property Type', 'Dwelling Type', 'Zip', 'Lp/SqFt', 'Neighborhood', 'DOM',
        'City', 'Zip', 'Bound Streets', 'Lot Size', 'Lot Description', 'Acres#', 'Age'])
        cur = self.crawler.to_db(
            INSERT,
            params=(self.crawler.date,
                    data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0],
                    listing_data['Property Type'],
                    listing_data['Dwelling Type'],
                    listing_data['City'],
                    listing_data['Zip'],
                    listing_data['Lp/SqFt'],
                    listing_data['Neighborhood'],
                    listing_data[ 'DOM'],
                    listing_data['Bound Streets'],
                    listing_data['Lot Size'],
                    listing_data['Lot Description'],
                    listing_data['Acres#'],
                    listing_data['Age'])
        )
        cur.execute('select * from testleads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))
@unittest.skip('testing only fq')
class TestMlsScraperSfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_7TH_9TH_MARIGNY_BYWATER)
        cls.soup = cls.crawler.single_line_view()
        conn = create_connection('config.cfg')
        create_database(conn, schema='testleadmachine')
        create_table(cls.crawler.conn, 'TESTLEADS', testcolumns)

    @classmethod
    def tearDownClass(cls):
        drop_table(cls.crawler.conn, 'TESTLEADS')
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    # def test_scrape_table_header(self):
    #     columns = self.crawler.scrape_table_header(self.soup)
    #     expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
    #     self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        self.assertTrue(len(data) > 0)

    def test_scrape_listing_info(self):
        data = self.crawler.get_listing_info(3, properties=['List Price','MLS Number','Zip'])
        self.assertEqual(3, len(data))

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        listing_data = self.crawler.get_listing_info(3, properties=['Property Type', 'Dwelling Type', 'Zip', 'Lp/SqFt', 'Neighborhood', 'DOM',
        'City', 'Zip', 'Bound Streets', 'Lot Size', 'Lot Description', 'Acres#', 'Age'])
        cur = self.crawler.to_db(
            INSERT,
            params=(self.crawler.date,
                    data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0],
                    listing_data['Property Type'],
                    listing_data['Dwelling Type'],
                    listing_data['City'],
                    listing_data['Zip'],
                    listing_data['Lp/SqFt'],
                    listing_data['Neighborhood'],
                    listing_data[ 'DOM'],
                    listing_data['Bound Streets'],
                    listing_data['Lot Size'],
                    listing_data['Lot Description'],
                    listing_data['Acres#'],
                    listing_data['Age'])
        )
        cur.execute('select * from testleads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))
@unittest.skip('testing only fq')
class TestMlsScraperMfMb(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(MF_7TH_9TH_MARIGNY_BYWATER)
        cls.soup = cls.crawler.single_line_view()
        conn = create_connection('config.cfg')
        create_database(conn, schema='testleadmachine')
        create_table(cls.crawler.conn, 'TESTLEADS', testcolumns)

    @classmethod
    def tearDownClass(cls):
        drop_table(cls.crawler.conn, 'TESTLEADS')
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    # def test_scrape_table_header(self):
    #     columns = self.crawler.scrape_table_header(self.soup)
    #     expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
    #     self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        self.assertTrue(len(data) > 0)

    def test_scrape_listing_info(self):
        data = self.crawler.get_listing_info(3, properties=['List Price','MLS Number','Zip'])
        self.assertEqual(3, len(data))

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        listing_data = self.crawler.get_listing_info(3, properties=['Property Type', 'Dwelling Type', 'Zip', 'Lp/SqFt', 'Neighborhood', 'DOM',
        'City', 'Zip', 'Bound Streets', 'Lot Size', 'Lot Description', 'Acres#', 'Age'])
        cur = self.crawler.to_db(
            INSERT,
            params=(self.crawler.date,
                    data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0],
                    listing_data['Property Type'],
                    listing_data['Dwelling Type'],
                    listing_data['City'],
                    listing_data['Zip'],
                    listing_data['Lp/SqFt'],
                    listing_data['Neighborhood'],
                    listing_data[ 'DOM'],
                    listing_data['Bound Streets'],
                    listing_data['Lot Size'],
                    listing_data['Lot Description'],
                    listing_data['Acres#'],
                    listing_data['Age'])
        )
        cur.execute('select * from testleads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))
@unittest.skip('testing only fq')
class TestMlsScraperSfLakeview(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_70119_70122_70124)
        cls.soup = cls.crawler.single_line_view()
        conn = create_connection('config.cfg')
        create_database(conn, schema='testleadmachine')
        create_table(cls.crawler.conn, 'TESTLEADS', testcolumns)

    @classmethod
    def tearDownClass(cls):
        drop_table(cls.crawler.conn, 'TESTLEADS')
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    # def test_scrape_table_header(self):
    #     columns = self.crawler.scrape_table_header(self.soup)
    #     expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
    #     self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        self.assertTrue(len(data) > 0)

    def test_scrape_listing_info(self):
        data = self.crawler.get_listing_info(3, properties=['List Price','MLS Number','Zip'])
        self.assertEqual(3, len(data))

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        listing_data = self.crawler.get_listing_info(3, properties=['Property Type', 'Dwelling Type', 'Zip', 'Lp/SqFt', 'Neighborhood', 'DOM',
        'City', 'Zip', 'Bound Streets', 'Lot Size', 'Lot Description', 'Acres#', 'Age'])
        cur = self.crawler.to_db(
            INSERT,
            params=(self.crawler.date,
                    data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0],
                    listing_data['Property Type'],
                    listing_data['Dwelling Type'],
                    listing_data['City'],
                    listing_data['Zip'],
                    listing_data['Lp/SqFt'],
                    listing_data['Neighborhood'],
                    listing_data[ 'DOM'],
                    listing_data['Bound Streets'],
                    listing_data['Lot Size'],
                    listing_data['Lot Description'],
                    listing_data['Acres#'],
                    listing_data['Age'])
        )
        cur.execute('select * from testleads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))
@unittest.skip('testing only fq')
class TestMlsScraperMfUptown(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(MF_70118_70125_70113_70130_70115)
        cls.soup = cls.crawler.single_line_view()
        conn = create_connection('config.cfg')
        create_database(conn, schema='testleadmachine')
        create_table(cls.crawler.conn, 'TESTLEADS', testcolumns)

    @classmethod
    def tearDownClass(cls):
        drop_table(cls.crawler.conn, 'TESTLEADS')
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    # def test_scrape_table_header(self):
    #     columns = self.crawler.scrape_table_header(self.soup)
    #     expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
    #     self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        self.assertTrue(len(data) > 0)

    def test_scrape_listing_info(self):
        data = self.crawler.get_listing_info(3, properties=['List Price','MLS Number','Zip'])
        self.assertEqual(3, len(data))

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        listing_data = self.crawler.get_listing_info(3, properties=['Property Type', 'Dwelling Type', 'Zip', 'Lp/SqFt', 'Neighborhood', 'DOM',
        'City', 'Zip', 'Bound Streets', 'Lot Size', 'Lot Description', 'Acres#', 'Age'])
        cur = self.crawler.to_db(
            INSERT,
            params=(self.crawler.date,
                    data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0],
                    listing_data['Property Type'],
                    listing_data['Dwelling Type'],
                    listing_data['City'],
                    listing_data['Zip'],
                    listing_data['Lp/SqFt'],
                    listing_data['Neighborhood'],
                    listing_data[ 'DOM'],
                    listing_data['Bound Streets'],
                    listing_data['Lot Size'],
                    listing_data['Lot Description'],
                    listing_data['Acres#'],
                    listing_data['Age'])
        )
        cur.execute('select * from testleads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))
@unittest.skip('testing only fq')
class TestMlsScraperSfUptown(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(SF_70118_70125_70113_70130_70115)
        cls.soup = cls.crawler.single_line_view()
        conn = create_connection('config.cfg')
        create_database(conn, schema='testleadmachine')
        create_table(cls.crawler.conn, 'TESTLEADS', testcolumns)

    @classmethod
    def tearDownClass(cls):
        drop_table(cls.crawler.conn, 'TESTLEADS')
        delete_database(cls.crawler.conn, schema='testleadmachine')
        cls.crawler.conn.close()

    def test_link_type(self):
        # print(type(self.crawler.searches[0]))
        # print(self.crawler.searches[0])
        # print(self.crawler.searches[0].attrs["href"])
        pass

    # def test_scrape_table_header(self):
    #     columns = self.crawler.scrape_table_header(self.soup)
    #     expected = ['Sent', 'Change Type', 'MLS #', 'S', 'Address', 'Current Price', 'Beds Total', 'FB', 'HB', 'Age Desc 1', 'Ap SF Lv Ar', 'Yr Blt']
    #     self.assertTrue(columns == expected)

    def test_scrape_table_data(self):
        data = self.crawler.scrape_table_columns(self.soup)
        self.assertTrue(len(data) > 0)

    def test_scrape_listing_info(self):
        data = self.crawler.get_listing_info(3, properties=['List Price','MLS Number','Zip'])
        self.assertEqual(3, len(data))

    def test_write_to_db(self):
        data = self.crawler.scrape_table_columns(self.soup)
        listing_data = self.crawler.get_listing_info(3, properties=['Property Type', 'Dwelling Type', 'Zip', 'Lp/SqFt', 'Neighborhood', 'DOM',
        'City', 'Zip', 'Bound Streets', 'Lot Size', 'Lot Description', 'Acres#', 'Age'])
        cur = self.crawler.to_db(
            INSERT,
            params=(self.crawler.date,
                    data['sent'][0],
                    data['changetype'][0],
                    data['mlsnum'][0],
                    data['address'][0],
                    data['price'][0],
                    data['beds'][0],
                    data['fullbath'][0],
                    data['halfbath'][0],
                    data['agedesc'][0],
                    data['sqft'][0],
                    data['built'][0],
                    listing_data['Property Type'],
                    listing_data['Dwelling Type'],
                    listing_data['City'],
                    listing_data['Zip'],
                    listing_data['Lp/SqFt'],
                    listing_data['Neighborhood'],
                    listing_data[ 'DOM'],
                    listing_data['Bound Streets'],
                    listing_data['Lot Size'],
                    listing_data['Lot Description'],
                    listing_data['Acres#'],
                    listing_data['Age'])
        )
        cur.execute('select * from testleads')
        results = cur.fetchall()
        self.assertEqual(1, len(results))

    @unittest.skip('not needed')
    def test_get_proxies(self):
        for i in range(10):
            url = SF_70118_70125_70113_70130_70115
            try:
                crawler = MlsCrawler(url)
            except:
                pass


if __name__ == '__main__':
    unittest.main()
