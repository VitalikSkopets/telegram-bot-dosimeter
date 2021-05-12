import os
import unittest
from unittest.mock import Mock
from handlers import Handlers

TOKEN = os.environ.get("TOKEN")
PASSWORD_MONGO_DB = os.environ.get("PASSWORD_MONGO_DB")

mock_update = Mock(name='mock update', return_value=
{'update_id': 529174731,
 'message': {
     'message_id': 4029,
     'date': 1620813558,
     'chat': {
         'id': 413818791,
         'type': 'private',
         'username': 'vitalik_sk',
         'first_name': 'Skopets',
         'last_name': 'Vitalik'
             },
     'text': '/help',
     'entities': [{'type': 'bot_command', 'offset': 0, 'length': 6}],
     'caption_entities': [],
     'photo': [],
     'new_chat_members': [],
     'new_chat_photo': [],
     'delete_chat_photo': False,
     'group_chat_created': False,
     'supergroup_chat_created': False,
     'channel_chat_created': False,
     'from': {
         'id': 413818791,
         'first_name': 'Skopets',
         'is_bot': False,
         'last_name': 'Vitalik',
         'username': 'vitalik_sk',
         'language_code': 'en'
             }
            }
 }
                   )
mock_update.effective_user = {'id': 413818791, 'first_name': 'Skopets', 'is_bot': False, 'last_name': 'Vitalik',
                              'username': 'vitalik_sk', 'language_code': 'en'
                              }

mock_context = Mock(name='mock context')


class TestHelp(unittest.TestCase):

    def test_help(self):
        result = Handlers.help(mock_update, mock_context)
        self.assertEqual(result, None)
        self.assertIsNone(result)
        print(mock_update.message.reply_text.call_count)


if __name__ == '__main__':
    unittest.main(verbosity=2)
