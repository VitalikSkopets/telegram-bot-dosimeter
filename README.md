# Telegram Bot Dosimeter

![GitHub top language](https://img.shields.io/github/languages/top/vitalikskopets/telegram-bot-dosimeter)
![GitHub License](https://img.shields.io/github/license/vitalikskopets/telegram-bot-dosimeter?style=flat)
![GitHub repo size](https://img.shields.io/github/repo-size/vitalikskopets/telegram-bot-dosimeter?style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/vitalikskopets/telegram-bot-dosimeter)

This bot can inform the user as of the current date about the radiation situation in Belarus and the level of equivalent dose of gamma radiation detected in the radiation monitoring network. Source: [rad.org.by](https://rad.org.by/monitoring/radiation)

One of the functions of the bot is to determine the distance to the nearest point of observation in the radiation monitoring network of the Ministry of Natural Resources and Environmental Protection of the Republic of Belarus. The specified function is available when the user sends the coordinates of its current geolocation.

The bot does not store the geographical coordinates of the user. However, the bot has implemented a long-term data storage function in the cloud store  [cloud.mongodb](https://cloud.mongodb.com/).
