import unittest
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ADMINISTRATIVE_DIVISION = {
    "Брестская область": ['Высокое', 'Пружаны', 'Брест', 'Ивацевичи', 'Пинск', 'Барановичи',
                          'Полесская, болотная', 'Дрогичин', 'Мокраны', 'Олтуш', 'Верхний Теребежов'],
    "Витебская область": ['Полоцк', 'Шарковщина', 'Лынтупы', 'Орша', 'Витебск', 'Нарочь, озерная',
                          'Верхнедвинск', 'Сенно'],
    "Гродненская область": ['Волковыск', 'Ошмяны', 'Лида', 'Гродно, АМСГ'],
    "Могилевская область": ['Могилев', 'Мстиславль', 'Славгорорд', 'Горки', 'Костюковичи', 'Бобруйск'],
    "Минск и Минская область": ['Минск', 'Слуцк', 'Вилейка', 'Борисов', 'Березино', 'Столбцы',
                                'Нарочь, озерная', 'Воложин'],
    "Гомельская область": ['Брагин', 'Мозырь', 'Василевичи', 'Жлобин', 'Октябрь', 'Житковичи',
                           'Гомель', 'Глушкевичи', 'Словечно', 'Словечно']
}


def get_html(html='https://rad.org.by/radiation.xml'):
    """ Функия отправляет get-звапрос и скрайпит https://rad.org.by/radiation.xml """
    response = requests.get(html, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def scraper(region="Гродненская область") -> None:
    """ Функция скрайпит html-структуру веб-ресурса https://rad.org.by/radiation.xml """
    points, indications = get_html().find_all('title'), get_html().find_all('rad')
    points.reverse()
    indications.reverse()
    zipped_values = zip(points, indications)
    zipped_list = list(zipped_values)
    indications_region, table = [], []
    for i in range(0, len(zipped_list)):
        if points[i].text in ADMINISTRATIVE_DIVISION["Гродненская область"]:
            indications_region.append(float(indications[i].text))
            new_point = points[i].text
            table.append('| {} | {:^13} |'.format(new_point, indications[i].text + ' мкЗв/ч'))
    avg_indication_region = sum(indications_region) / len(indications_region)


class ScraperTestCase(unittest.TestCase):

    def test_scraper_1(self):
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        indications_region, table = [], []
        for i in range(0, len(zipped_list)):
            if points[i].text in ADMINISTRATIVE_DIVISION["Гродненская область"]:
                indications_region.append(float(indications[i].text))
        self.assertGreater(len(indications), 0)

    def test_scraper_2(self):
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        indications_region, table = [], []
        for i in range(0, len(zipped_list)):
            if points[i].text in ADMINISTRATIVE_DIVISION["Гродненская область"]:
                indications_region.append(float(indications[i].text))
        self.assertIn(0.1, indications_region)

    def test_scraper_3(self):
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        indications_region, table = [], []
        for i in range(0, len(zipped_list)):
            if points[i].text in ADMINISTRATIVE_DIVISION["Гродненская область"]:
                indications_region.append(float(indications[i].text))
                new_point = points[i].text
                table.append('| {} | {:^13} |'.format(new_point, indications[i].text + ' мкЗв/ч'))
        self.assertEqual(len(table), 4)

    def test_scraper_4(self):
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        indications_region, table = [], []
        for i in range(0, len(zipped_list)):
            if points[i].text in ADMINISTRATIVE_DIVISION["Гродненская область"]:
                indications_region.append(float(indications[i].text))
        avg_indication_region = sum(indications_region) / len(indications_region)
        self.assertIsInstance(avg_indication_region, float)


if __name__ == '__main__':
    unittest.main(verbosity=2)
