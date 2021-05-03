import os
from typing import Final
from loguru import logger
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters
                          )
from handlers import Handlers

logger.add('debug.log', level='DEBUG', rotation='1 MB', compression='zip')


@logger.catch()
def main() -> None:
    """
    Функция инициализации и запуска бота - объекта класса Updater из модуля python-telegram-bot
    :return: None
    """
    bot: Final = Updater(os.environ['TOKEN'])

    dp: Final = bot.dispatcher
    dp.add_handler(CommandHandler('start', Handlers.start))
    dp.add_handler(CommandHandler('help', Handlers.help))
    dp.add_handler(MessageHandler(Filters.location, Handlers.geolocation))
    dp.add_handler(MessageHandler(Filters.regex('^(Радиационный мониторинг)$'), Handlers.radioactive_monitoring))
    dp.add_handler(MessageHandler(Filters.regex('^(Пункты наблюдения)$'), Handlers.monitoring_points))
    dp.add_handler(MessageHandler(Filters.regex('^(Брестская область)$'), Handlers.scraper_Brest))
    dp.add_handler(MessageHandler(Filters.regex('^(Витебская область)$'), Handlers.scraper_Vitebsk))
    dp.add_handler(MessageHandler(Filters.regex('^(Гомельская область)$'), Handlers.scraper_Gomel))
    dp.add_handler(MessageHandler(Filters.regex('^(Гродненская область)$'), Handlers.scraper_Grodno))
    dp.add_handler(MessageHandler(Filters.regex('^(Минск и Минская область)$'), Handlers.scraper_Minsk))
    dp.add_handler(MessageHandler(Filters.regex('^(Могилевская область)$'), Handlers.scraper_Mogilev))
    dp.add_handler(MessageHandler(Filters.regex('^(Главное меню)$'), Handlers.master_menu))
    dp.add_handler(MessageHandler(Filters.text, Handlers.messages))

    # if os.environ['HEROKU_APP_NAME'] is False:
    #     logger.info('Start Bot in pooling mode')
    #     bot.start_polling()
    #     bot.idle()
    # else:
    #     bot.start_webhook(listen='0.0.0.0',
    #                       port=int(os.environ['PORT']),
    #                       url_path=os.environ['TOKEN'],
    #                       webhook_url=f"https://{os.environ['HEROKU_APP_NAME']}.herokuapp.com/{os.environ['TOKEN']}"
    #                       )
    #     logger.info('Start Bot in webhook mode')
    #     bot.idle()

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
