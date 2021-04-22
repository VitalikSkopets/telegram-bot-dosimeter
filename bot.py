from loguru import logger
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from handlers import start, help, geolocation, radioactive_monitoring, scraper, get_text_messages

logger.add('debug.log', level='DEBUG', rotation='1 MB', compression='zip')


@logger.catch()
def main():
    """
    Функция инициализации и запуска бота - объекта класса Updater из модуля python-telegram-bot
    :return: None
    """
    bot = Updater(TOKEN)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.location, geolocation))
    dp.add_handler(MessageHandler(Filters.regex('^(Радиационный мониторинг)$'), radioactive_monitoring))
    dp.add_handler(MessageHandler(Filters.regex('^(Пункты наблюдения)$'), scraper))
    dp.add_handler(MessageHandler(Filters.text, get_text_messages))

    logger.info('Start Bot')
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
