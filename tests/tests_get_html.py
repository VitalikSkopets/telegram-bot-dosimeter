import unittest
from bs4 import BeautifulSoup
from utilities import get_html


class TestGetHtml(unittest.TestCase):

    def test_get_html_1(self):
        self.assertTrue(get_html())

    def test_get_html_2(self):
        self.assertIsInstance(get_html(), BeautifulSoup)


@unittest.skip('test works when a wrong url is entered')
class TestBadGetHtml(unittest.TestCase):

    def test_bad_get_html(self):
        self.assertRaises(Exception, get_html())


if __name__ == "__main__":
    unittest.main(verbosity=2)
