import unittest


def help(text: str, tamplate='/help') -> str:
    """ Функция-обработчик команды /help """
    if text == tamplate:
        return "Бот-дозиметр может информировать..."
    return "unknown message"


class HelpTestCase(unittest.TestCase):
    def test_help_1(self):
        result = help('/help')
        self.assertEqual(result, "Бот-дозиметр может информировать...")

    def test_help_2(self):
        result = help('/start')
        self.assertEqual(result, "unknown message")


if __name__ == '__main__':
    unittest.main()
