import unittest
from unittest.mock import Mock
from utilities import scraper


mock_update = Mock()
mock_update.effective_user = {'first_name': 'Test_name'}


class TestScraper(unittest.TestCase):

    def test_scraper(self):
        result = scraper(update=mock_update, region=['Волковыск', 'Ошмяны', 'Лида', 'Гродно, АМСГ'])
        self.assertEqual(result, None)
        self.assertIsNone(result)
        print(mock_update.message.reply_text.call_count)


@unittest.skip('test works when a wrong url is entered')
class TestBadScraper(unittest.TestCase):

    def test_bad_scraper(self):
        self.assertRaises(Exception, scraper(update=mock_update, region='Волковыск'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
