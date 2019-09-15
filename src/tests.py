"""Tests

"""

import unittest

import datetime

from scraper import BaseCrawler
from create_tables import create_database
from create_tables import delete_database
from create_tables import create_tables
from create_tables import drop_tables
from sql_queries import leads_insert

class TestScraper(unittest.TestCase):
    """

    """

    def test_no_config(self):
        base_crawler = BaseCrawler()
        self.assertTrue(True)

    def test_config(self):
        base_crawler = BaseCrawler(conn_info='config.cfg')
        self.assertTrue(True)

    def test_config_fail(self):
        try:
            base_crawler = BaseCrawler(conn_info='notmyconfig.cfg')
        except KeyError:
            self.assertTrue(True)

class TestDb(unittest.TestCase):
    """Database tests

    """
    @classmethod
    def setUpClass(cls):
        """Create the testing database
        """
        create_database('config.cfg', schema='testleadmachine')
        cls.conn = BaseCrawler().conn

    @classmethod
    def tearDownClass(cls):
        """Delete the testing database
        """
        delete_database(cls.conn, schema='testleadmachine')
        drop_tables(cls.conn)
        cls.conn.close()

    def setUp(self):
        self.cur = self.conn.cursor()

    def tearDown(self):
        pass

    def test_create_tables(self):
        create_tables(self.conn)
        self.cur.execute('select * from leads')
        results = self.cur.fetchall()
        # results is an empty list
        self.assertEqual(0, len(results))

    def test_insert_data(self):
        self.cur = self.conn.cursor()
        self.cur.execute(leads_insert, [datetime.datetime(2019,1,1),'varchar',1,'varchar',1,1,1,1,'varchar',1,1])
        self.cur.execute('select * from leads')
        results = self.cur.fetchall()
        self.assertEqual(1, len(results))

    # def test_insert_duplicate_data(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
