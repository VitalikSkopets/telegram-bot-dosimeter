import unittest


def start(text: str, tamplate='/start') -> str:
    """ Функция-обработчик команды /start """
    if text == tamplate:
        return "Приятно познакомится..."
    return "unknown message"


class StartTestCase(unittest.TestCase):
    def test_start_1(self):
        result = start('/start')
        self.assertEqual(result, "Приятно познакомится...")

    def test_start_2(self):
        result = start('/help')
        self.assertEqual(result, "unknown message")


if __name__ == '__main__':
    unittest.main()
