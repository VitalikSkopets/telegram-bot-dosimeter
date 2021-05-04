import unittest
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from geopy import distance

LOCATION_OF_MONITORING_POINTS = {
    'Могилев': (53.69298772769127, 30.375068475712993),
    'Мстиславль': (54.025123497951235, 31.742790754635983),
    'Полоцк': (55.47475184602021, 28.751296645976183),
    'Шарковщина': (55.36281482842422, 27.456996363944278),
    'Минск': (53.92751824354786, 27.63548838979854),
    'Лынтупы': (55.04878637860638, 26.306634538263953),
    'Высокое': (52.366928433095, 23.38374438625246),
    'Пружаны': (52.567268449727045, 24.48545241420398),
    'Слуцк': (53.05284098247522, 27.552283199561725),
    'Брагин': (51.7969974359342, 30.246689891878724),
    'Орша': (54.503170699795774, 30.443815788156527),
    'Мозырь': (52.036635775856084, 29.1925370196736),
    'Славгорорд': (53.45088516337511, 31.003458658160586),
    'Василевичи': (52.25207675198943, 29.838848231201965),
    'Жлобин': (52.89414619807851, 30.043705893277984),
    'Горки': (54.30393502455042, 30.94344246329931),
    'Волковыск': (53.16692103793095, 24.448995268762964),
    'Октябрь': (52.63342658653018, 28.883476209528087),
    'Костюковичи': (53.35847386774336, 32.070027796122154),
    'Брест': (52.116580901478635, 23.685652135212752),
    'Бобруйск': (53.20853347538013, 29.127272432117724),
    'Ивацевичи': (52.716654759080775, 25.350471424000386),
    'Вилейка': (54.48321442087189, 26.89989831916185),
    'Борисов': (54.26563317790094, 28.49760585109516),
    'Житковичи': (52.21411222651425, 27.870082634924596),
    'Ошмяны': (54.43300284193779, 25.935350063150867),
    'Березино': (53.82838181057285, 28.99727106523084),
    'Пинск': (52.12223760297976, 26.111811093605997),
    'Витебск': (55.25257562100984, 30.250042135934226),
    'Лида': (53.90227318372977, 25.32336091231988),
    'Барановичи': (53.13190185894763, 25.97158074066798),
    'Столбцы': (53.46677208676115, 26.732607935963017),
    'Полесская, болотная': (52.29983981155924, 26.667029013394274),
    'Дрогичин': (52.20004370649066, 25.0838433995118),
    'Гомель': (52.402061468751455, 30.963081201303428),
    'Нарочь, озерная': (54.899256667266, 26.684290791688372),
    'Воложин': (54.10018849587838, 26.51694607389268),
    'Верхнедвинск': (55.8208765412649, 27.940101948630605),
    'Сенно': (54.80456568197694, 29.687798174910593),
    'Гродно, АМСГ': (53.60193676812893, 24.05807929514318),
    'Мокраны': (51.83469016263843, 24.262048260884608),
    'Олтуш': (51.69107406162166, 23.97093118533709),
    'Верхний Теребежов': (51.83600602350391, 26.725999562270026),
    'Глушкевичи': (51.61087690551236, 27.825665051237728),
    'Словечно': (51.63093077915665, 29.068442241735667),
    'Новая Иолча': (51.49095727903912, 30.531611339649682),
}


def get_html(html='https://rad.org.by/radiation.xml'):
    """ Функия отправляет get-звапрос и скрайпит https://rad.org.by/radiation.xml """
    response = requests.get(html, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def geolocation():
    """ Функция-обработчик нажатия кнопки "Отправить мою геолокацию" """

    coordinates = (53.68043632625287, 27.421918985736937)
    distance_list = []
    for point, location in LOCATION_OF_MONITORING_POINTS.items():
        distance_list.append((distance.distance(coordinates, location).km, point))
    min_distance = min(distance_list)
    points, indications = get_html().find_all('title'), get_html().find_all('rad')
    points.reverse()
    indications.reverse()
    zipped_values = zip(points, indications)
    zipped_list = list(zipped_values)
    for i in range(0, len(zipped_list)):
        if min_distance[1] == points[i].text:
            return (f'{min_distance[0]:.3f} до ближайшего пункта наблюдения"{min_distance[1]}".\n\n Уровень '
                    f'эквивалентной дозым радиации составляет {indications[i].text} мкЗв/ч.'
                    )
            break


class GeolocationTestCase(unittest.TestCase):

    def test_geolocation_1(self):
        coordinates = (53.68043632625287, 27.421918985736937)
        distance_list = []
        for point, location in LOCATION_OF_MONITORING_POINTS.items():
            distance_list.append((distance.distance(coordinates, location).km, point))
        self.assertGreater(len(distance_list), 0)

    def test_geolocation_2(self):
        coordinates = (53.68043632625287, 27.421918985736937)
        distance_list = []
        for point, location in LOCATION_OF_MONITORING_POINTS.items():
            distance_list.append((distance.distance(coordinates, location).km, point))
        min_distance = min(distance_list)
        self.assertGreater(len(min_distance), 0)

    def test_geolocation_3(self):
        coordinates = (53.68043632625287, 27.421918985736937)
        distance_list = []
        for point, location in LOCATION_OF_MONITORING_POINTS.items():
            distance_list.append((distance.distance(coordinates, location).km, point))
        min_distance = min(distance_list)
        self.assertIsInstance(min_distance[0], float)

    def test_geolocation_4(self):
        points, indications= get_html().find_all('title'), get_html().find_all('rad')
        self.assertNotEqual(len(indications), len(points))

    def test_geolocation_5(self):
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        self.assertIsInstance(zipped_list, list)

    def test_geolocation_6(self):
        points, indications= get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        self.assertEqual(len(indications), len(zipped_list))

    def test_geolocation_7(self):
        points, indications= get_html().find_all('title'), get_html().find_all('rad')
        self.assertNotEqual(len(indications), len(points))


if __name__ == '__main__':
    unittest.main(verbosity=2)
