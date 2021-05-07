import unittest
from unittest import TestCase
from pymock import PyMock, Is
from utilities import scraper


class Update:

    def __init__(self, message='Text_message'):
        self.message = message

    def effective_user(self):
        return {'first_name': 'Test_name'}


class Message:

    def reply_text(self):
        return f'Hello world'


class ScraperTestCase(TestCase):

    def test_return_object(self):
        post = scraper(Update, region=dict(key='Гродненская область', values=['Гродно', 'Волковыск']))
        mock = PyMock.create(Update)
        PyMock.setup(mock.get_post(123)).returns(post)

    def test_scraper_1(self):
        pass


   if __name__ == '__main__':
    unittest.main(verbosity=2)
