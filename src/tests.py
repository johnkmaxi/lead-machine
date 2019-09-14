"""Tests

"""

import unittest

from scraper import BaseCrawler
from create_tables import create_database
from create_tables import delete_database
from create_tables import create_tables
from create_tables import drop_tables

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
    def setUp(self):
        """Create the testing database
        """
        create_database('config.cfg', schema='testleadmachine')
        self.conn = BaseCrawler().conn

    def tearDown(self):
        """Delete the testing database
        """
        delete_database(self.conn, schema='testleadmachine')
        drop_tables(self.conn)
        self.conn.close()

    def test_create_tables(self):
        create_tables(self.conn)

    def test_insert_data(self):
        pass

    def test_insert_duplicate_data(self):
        pass

if __name__ == '__main__':
    unittest.main()
