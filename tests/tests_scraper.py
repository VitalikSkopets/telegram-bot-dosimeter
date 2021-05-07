import unittest
from unittest import TestCase
from unittest.mock import Mock
from utilities import scraper

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

update = Mock()
update.effective_user = {'first_name': 'Test_name'}


class ScraperTestCase(TestCase):

    def test_scraper_1(self):
        result = scraper(update=update, region=ADMINISTRATIVE_DIVISION.get('Брестская область'))
        self.assertEqual(result, None)
        self.assertIsNone(result, None)
        print(update.message.reply_text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
