import os
import unittest
from unittest.mock import Mock
from handlers import Handlers

TOKEN = os.environ.get("TOKEN")
PASSWORD_MONGO_DB = os.environ.get("PASSWORD_MONGO_DB")

mock_update = Mock(name='mock update')
mock_context = Mock(name='mock context')
mock_update.effective_user = {'id': 413818791, 'first_name': 'Skopets', 'is_bot': False, 'last_name': 'Vitalik',
                              'username': 'vitalik_sk', 'language_code': 'en'
                              }




class TestHelp(unittest.TestCase):

    def test_help(self):
        Handlers.help(mock_update, mock_context)
        self.assertGreater(mock_update.message.reply_text.call_count, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
