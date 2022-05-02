# Dosimeter Telegram Bot
## Description

This bot can inform the user as of the current date about the radiation situation in Belarus and the level of equivalent dose of gamma radiation detected in the radiation monitoring network. Source: [rad.org.by](https://rad.org.by/monitoring/radiation)

One of the functions of the bot is to determine the distance to the nearest point of observation in the radiation monitoring network of the Ministry of Natural Resources and Environmental Protection of the Republic of Belarus. The specified function is available when the user sends the coordinates of its current geolocation.

The bot does not store the geographical coordinates of the user. However, the bot has implemented a long-term data storage function in the cloud store  [cloud.mongodb](https://cloud.mongodb.com/). The following information transmitted by [Telegram.org](https://telegram.org/) servers according to HTTPS protocol should be collected and subsequently stored.:

- first name
- last name
- user name

### Implementing asymmetric encryption of RSA data in code using a cryptographic library:
```python
import rsa

class DB:
    mdb: Final = MongoClient(MONGODB_REF)[MONGO_DB]

    def create_collection(user: dict[str, any]) -> dict[str, any]:
        current_user = {'user_id': user['id'],
                        'first_name': Crypt.encrypt(user['first_name']),
                        'last_name': Crypt.encrypt(user['last_name']),
                        'user_name': Crypt.encrypt(user['username'])

def encrypt(line: str, pubkey=__get_pubkey) -> str:
    if line is not None:
        token = rsa.encrypt(line.encode(), pubkey())
        return token
```
Telegram users' specified personal data are **encrypted** using the RSA asymmetric cryptographic encryption algorithm before entering them into the database, which guarantees confidentiality even if third parties gain access to the database. 

### Configuration file
##### config.py

```python
import os
from typing import Final

TOKEN: Final = os.environ["TOKEN"]  # token Telegram Bot API
MONGODB_REF = "mongodb+srv://DosimeterBot:dG7ntC7sa1RrDpBp@cluster.s3cxd.mongodb.net/users_db?retryWrites=true&w" \
              "=majority"
MONGO_DB: Final = "users_db"
LOGIN_MONGO_DB: Final = "DosimeterBot"
PASSWORD_MONGO_DB: Final = os.environ["PASSWORD_MONGO_DB"]
URL1: Final = 'https://rad.org.by/radiation.xml'
URL2: Final = 'https://rad.org.by/monitoring/radiation'

LOCATION_OF_MONITORING_POINTS = {'Могилев': (53.69298772769127, 30.375068475712993),
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
```
### List of external dependencies
##### requirements.txt
```python
APScheduler==3.6.3
asgiref==3.3.4
beautifulsoup4==4.9.3
certifi==2020.12.5
cffi==1.14.5
chardet==4.0.0
colorama==0.4.4
dnspython==2.1.0
emoji==1.2.0
fake-useragent==0.1.11
geographiclib==1.50
geopy==2.1.0
idna==2.10
loguru==0.5.3
pycparser==2.20
pymongo==3.11.3
python-telegram-bot==13.4.1
pytz==2021.1
requests==2.25.1
six==1.15.0
soupsieve==2.2.1
sqlparse==0.4.1
tornado==6.1
tzlocal==2.1
urllib3==1.26.4
win32-setctime==1.0.3
rsa~=4.7.2
```
#### Clone with HTTPS
```python
    https://gitlab.itrexgroup.com/vitaly.skopets/telegram-bot-desimeter.git
```
#### Clone with SSH
```python
    git@gitlab.itrexgroup.com:vitaly.skopets/telegram-bot-desimeter.git
```
