import os
from pathlib import Path
import telebot
from dotenv import load_dotenv

from selenium_main import parse_data_from_site

# load environment variables
BASE_DIR = Path(__file__).resolve().parent
dot_env = BASE_DIR / '.env'
load_dotenv(dotenv_path=dot_env)


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(
            message.chat.id,
            f'Привет, я бот, который помогает узнать информацию по Вашему заказ-наряду. '
            f'Введите его номер (например 2201010)',

        )

    @bot.message_handler(content_types=['text'])
    def send_message(message):
        response = parse_data_from_site(message.text)
        bot.send_message(
            message.chat.id,
            response,
        )

    bot.infinity_polling()


def main():
    token = os.getenv('API_BOT')
    telegram_bot(token)


if __name__ == '__main__':
    main()
