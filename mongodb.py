import datetime
from pymongo import MongoClient
from config import MONGODB_REF, MONGO_DB

mdb = MongoClient(MONGODB_REF)[MONGO_DB]
today = datetime.datetime.today().strftime("%a %d-%b-%Y %H-%M-%S")


def add_db_send_welcom(mdb, message_inf):
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'date': today
            }
    mdb.send_welcom.insert_one(user)


def add_db_send_help(mdb, message_inf):
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'date': today
            }
    mdb.send_help.insert_one(user)


def add_db_get_text_messages(mdb, message_inf):
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'date': today
            }
    mdb.get_text_messages.insert_one(user)


def add_db_radioactive_monitoring(mdb, message_inf):
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'date': today
            }
    mdb.radioactive_monitoring.insert_one(user)


def add_db_scraper(mdb, message_inf):
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'date': today
            }
    mdb.scraper.insert_one(user)


def add_db_geolocation(mdb, message_inf):
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'date': today
            }
    mdb.geolocation.insert_one(user)