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

if __name__ == '__main__':
    unittest.main()
