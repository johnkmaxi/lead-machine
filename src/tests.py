"""Tests

"""

import unittest

import datetime

from scraper import BaseCrawler
from scraper import MlsCrawler
from create_tables import create_database
from create_tables import delete_database
from create_tables import create_tables
from create_tables import drop_tables
from sources import my_searches
from sql_queries import leads_insert

# class TestScraper(unittest.TestCase):
#     """
#
#     """
#
#     @classmethod
#     def setUpClass(cls):
#         """Create the testing database
#         """
#         create_database('config.cfg', schema='testleadmachine')
#         cls.test_crawler = BaseCrawler()
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
#         base_crawler = BaseCrawler()
#         self.assertTrue(True)
#
#     def test_config(self):
#         base_crawler = BaseCrawler(conn_info='config.cfg')
#         self.assertTrue(True)
#
#     def test_config_fail(self):
#         try:
#             base_crawler = BaseCrawler(conn_info='notmyconfig.cfg')
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
#         cls.conn = BaseCrawler().conn
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
        cls.crawler = MlsCrawler(my_searches)


    def test_collect_search_list(self):
        self.assertEqual(9, len(self.crawler.searches))

if __name__ == '__main__':
    unittest.main()
