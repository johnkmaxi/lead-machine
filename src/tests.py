"""Tests

"""

import unittest

import datetime

from db import BaseDb
from scraper import BaseCrawler
from scraper import MlsCrawler
from create_tables import create_database
from create_tables import delete_database
from create_tables import create_tables
from create_tables import drop_tables
from sources import my_searches
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
#         delete_database(cls.test_crawler.conn, schema='testleadmachine')
#         drop_tables(cls.test_crawler.conn)
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
# class TestDb(unittest.TestCase):
#     """Database tests
#
#     """
#     @classmethod
#     def setUpClass(cls):
#         """Create the testing database
#         """
#         create_database('config.cfg', schema='testleadmachine')
#         cls.conn = BaseDb().conn
#
#     @classmethod
#     def tearDownClass(cls):
#         """Delete the testing database
#         """
#         delete_database(cls.conn, schema='testleadmachine')
#         drop_tables(cls.conn)
#         cls.conn.close()
#
#     def setUp(self):
#         self.cur = self.conn.cursor()
#
#     def tearDown(self):
#         pass
#
#     def test_create_tables(self):
#         create_tables(self.conn)
#         self.cur.execute('select * from leads')
#         results = self.cur.fetchall()
#         # results is an empty list
#         self.assertEqual(0, len(results))
#
#     def test_insert_data(self):
#         self.cur.execute(leads_insert, [datetime.datetime(2019,1,1),'varchar',1,'varchar',1,1,1,1,'varchar',1,1])
#         self.cur.execute('select * from leads')
#         results = self.cur.fetchall()
#         self.assertEqual(1, len(results))
#
#     def test_insert_duplicate_data(self):
#         self.cur.execute(leads_insert, [datetime.datetime(2019,1,1),'varchar',1,'varchar',1,1,1,1,'varchar',1,1])
#         self.cur.execute('select * from leads')
#         results = self.cur.fetchall()
#         self.assertEqual(1, len(results))

class TestMlsScraper(unittest.TestCase):
    """MLS scraping tests

    """

    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        cls.crawler = MlsCrawler(my_searches, html_file='mls_source_html_test.html')

    def test_read_from_file(self):
        self.assertIs(type(self.crawler.source_html), str)

    def test_collect_search_list_len(self):
        self.assertEqual(9, len(self.crawler.searches))

    def test_collect_search_list_names(self):
        link_text = [x.text.strip() for x in self.crawler.searches]
        self.assertTrue("Single family: FQ & Iberville" in link_text)
        self.assertTrue("Multi-family: 7& 9th wards, Marigny/Bywater" in link_text)
        self.assertTrue("Single family: 7th & 9th wards, Marigy/Bywater" in link_text)
        self.assertTrue("Multi-family: 70114, 70131" in link_text)
        self.assertTrue("Single family: 70114, 70131" in link_text)
        self.assertTrue("Multi-family: 70119, 70122, 70124" in link_text)
        self.assertTrue("Single family: 70119, 70122, 70124" in link_text)
        self.assertTrue("Multi-family: 70118 70125 70113 70130 70115" in link_text)
        self.assertTrue("Single family: 70118 70125 70113 70130 70115" in link_text)

if __name__ == '__main__':
    unittest.main()
