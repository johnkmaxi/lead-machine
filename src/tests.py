"""Tests

"""

import unittest

from scraper import BaseCrawler

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
        pass

    def tearDown(self):
        """Delete the testing database
        """
        pass

    def test_create_tables(self):
        pass

    def test_insert_data(self):
        pass

    def test_insert_duplicate_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
