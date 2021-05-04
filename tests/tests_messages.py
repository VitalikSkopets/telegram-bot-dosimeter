import unittest

greeting = ['hello', 'hi', 'hey', 'привет', 'салют', 'здарова', 'здравствуй', 'здравствуйте', 'добрый день',
            'добрый вечер', 'доброе утро', 'доброго дня', 'хелоу', 'бонжур', 'привестствую', 'здрасте',
            'какая встреча', 'рад встрече', 'хай', 'здравия желаю', 'приветик', 'доброго времени суток',
            'здорова', 'здорово', 'мое почтение', 'приветствую тебя', 'сердечно приветствую', 'how are you',
            'what’s up', 'whats up', 'hello there', 'howdy', 'hiya', 'yo', 'how do you do', 'good morning',
            'good afternoon', 'good evening', 'peek-a-boo', 'peek a boo', 'hi mister', 'ahoy'
            ]


def messages(text: str, greeting: list) -> str:
    """ Функция-обработчик тествового сообщенаия пользователя """
    if text.lower() in greeting:
        return "Привет, User"
    else:
        return "unknown message"


class MessageTestCase(unittest.TestCase):
    def test_messages_1(self):
        result = messages('hello', greeting)
        self.assertEqual(result, "Привет, User")

    def test_messages_2(self):
        result = messages('салют', greeting)
        self.assertEqual(result, "Привет, User")

    def test_messages_3(self):
        result = messages('good morning', greeting)
        self.assertEqual(result, "Привет, User")

    def test_messages_4(self):
        result = messages('klsjdgbvo', greeting)
        self.assertEqual(result, "unknown message")

    def test_messages_5(self):
        result = messages('25656', greeting)
        self.assertEqual(result, "unknown message")


if __name__ == '__main__':
    unittest.main()
