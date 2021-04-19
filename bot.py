import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from handlers import send_welcome, send_help, geolocation, radioactive_monitoring, scraper, get_text_messages

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def main():
    bot = Updater(TOKEN)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', send_welcome))
    dp.add_handler(CommandHandler('help', send_help))
    dp.add_handler(MessageHandler(Filters.location, geolocation))
    dp.add_handler(MessageHandler(Filters.regex('^(Радиационный мониторинг)$'), radioactive_monitoring))
    dp.add_handler(MessageHandler(Filters.regex('^(Пункты наблюдения)$'), scraper))
    dp.add_handler(MessageHandler(Filters.text, get_text_messages))

    logging.info('Start Bot')
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
