import os
from loguru import logger
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters
                          )
from handlers import (start,
                      help,
                      geolocation,
                      radioactive_monitoring,
                      monitoring_points,
                      scraper_Brest,
                      scraper_Vitebsk,
                      scraper_Gomel,
                      scraper_Grodno,
                      scraper_Minsk,
                      scraper_Mogilev,
                      messages
                      )

logger.add('debug.log', level='DEBUG', rotation='1 MB', compression='zip')


@logger.catch()
def main():
    """
    Функция инициализации и запуска бота - объекта класса Updater из модуля python-telegram-bot
    :return: None
    """
    bot = Updater(os.environ['TOKEN'])

    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.location, geolocation))
    dp.add_handler(MessageHandler(Filters.regex('^(Радиационный мониторинг)$'), radioactive_monitoring))
    dp.add_handler(MessageHandler(Filters.regex('^(Пункты наблюдения)$'), monitoring_points))
    dp.add_handler(MessageHandler(Filters.regex('^(Брестская область)$'), scraper_Brest))
    dp.add_handler(MessageHandler(Filters.regex('^(Витебская область)$'), scraper_Vitebsk))
    dp.add_handler(MessageHandler(Filters.regex('^(Гомельская область)$'), scraper_Gomel))
    dp.add_handler(MessageHandler(Filters.regex('^(Гродненская область)$'), scraper_Grodno))
    dp.add_handler(MessageHandler(Filters.regex('^(Минск и Минская область)$'), scraper_Minsk))
    dp.add_handler(MessageHandler(Filters.regex('^(Могилевская область)$'), scraper_Mogilev))
    dp.add_handler(MessageHandler(Filters.text, messages))

    # if os.environ['HEROKU_APP_NAME'] is None:     # не по питоняче
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
