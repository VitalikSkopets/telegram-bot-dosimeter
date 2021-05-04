import unittest
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url1 = 'https://rad.org.by/radiation.xml'
url2 = 'https://rad.org.by/monitoring/radiation'

def get_html(url) -> BeautifulSoup:
    """ Функия отправляет get-звапрос и скрайпит url1 либо url2 """
    response = requests.get(url, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

class GetHtmlTest(unittest.TestCase):

    def test_get_html_1(self):
        response = requests.get(url1, headers={'User-Agent': UserAgent().random})
        self.assertEqual(response.status_code, 200)

    def test_get_html_2(self):
        response = requests.get(url2, headers={'User-Agent': UserAgent().random})
        self.assertEqual(response.status_code, 200)

    def test_get_html_3(self):
        result = get_html(url2)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
