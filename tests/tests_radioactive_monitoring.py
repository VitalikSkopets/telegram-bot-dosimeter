import unittest
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://rad.org.by/monitoring/radiation'


def get_html(html) -> BeautifulSoup:
    """ Функия отправляет get-звапрос и скрайпит https://rad.org.by/radiation.xml """
    response = requests.get('https://rad.org.by/radiation.xml', headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def radioactive_monitoring(html):
    """ Функция-обработчик нажатия кнопки "Радиационный мониторинг" """
    response = requests.get(html, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.text, 'html.parser')
    text_lst = str(soup.find_all('span'))
    pattern = r"(?:...*)(радиационная...*загрязнения)(?:<\/span>)"
    text = re.findall(pattern, text_lst)
    print(type(text))
    return text


answer = [
          'радиационная обстановка на территории Республики Беларусь стабильная, мощность дозы (МД) гамма-излучения '
          'соответствует установившимся многолетним значениям. Как и прежде, повышенный уровень МД гамма-излучения '
          'зарегистрирован в пункте наблюдения города Брагин, находящегося в зоне радиоактивного загрязнения'
          ]


class RadioactiveMonitoringTestCase(unittest.TestCase):

    def test_radioactive_monitoring_1(self):
        result = radioactive_monitoring(url)
        self.assertEqual(result, answer)

    def test_radioactive_monitoring_2(self):
        result = radioactive_monitoring(url)
        self.assertIn(answer[0], result)

    def test_radioactive_monitoring_3(self):
        result = radioactive_monitoring(url)
        self.assertCountEqual(result, answer)

    def test_radioactive_monitoring_4(self):
        result = radioactive_monitoring(url)
        self.assertListEqual(result, answer)

    def test_radioactive_monitoring_5(self):
        result = radioactive_monitoring(url)
        self.assertTrue(result)

    def test_radioactive_monitoring_6(self):
        response = requests.get(url, headers={'User-Agent': UserAgent().random})
        soup = BeautifulSoup(response.text, 'html.parser')
        text_lst = str(soup.find_all('span'))
        self.assertRegex(text_lst, r"(?:...*)(радиационная...*загрязнения)(?:<\/span>)")

    def test_radioactive_monitoring_7(self):
        indications = get_html('https://rad.org.by/radiation.xml').find_all('rad')
        avg_indication = sum([float(indication.text) for indication in indications]) / len(indications)
        self.assertTrue(avg_indication)

    def test_radioactive_monitoring_8(self):
        indications = get_html('https://rad.org.by/radiation.xml').find_all('rad')
        avg_indication = sum([float(indication.text) for indication in indications]) / len(indications)
        self.assertIsInstance(avg_indication, float)

    def test_radioactive_monitoring_9(self):
        indications = get_html('https://rad.org.by/radiation.xml').find_all('rad')
        avg_indication = sum([float(indication.text) for indication in indications]) / len(indications)
        self.assertIs(type(avg_indication), float)

    def test_radioactive_monitoring_10(self):
        indications = get_html('https://rad.org.by/radiation.xml').find_all('rad')
        avg_indication = sum([float(indication.text) for indication in indications]) / len(indications)
        self.assertGreater(avg_indication, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
