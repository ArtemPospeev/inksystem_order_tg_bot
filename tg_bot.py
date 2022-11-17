import os
from pathlib import Path
import telebot
from dotenv import load_dotenv
from telebot import types

from selenium_main import parse_data_from_site

# load environment variables
BASE_DIR = Path(__file__).resolve().parent
FILE_DIR = BASE_DIR / 'files_ru/'
CODING = 'UTF-8'
dot_env = BASE_DIR / '.env'
load_dotenv(dotenv_path=dot_env)


def give_data_from_file(file):
    ''' Читает файл, вытаскивает содержимое'''
    with open(FILE_DIR / (file + '.txt'), 'r', encoding=CODING) as f:
        text = f.read()
    return text


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton('Статус ремонта'),
                   types.KeyboardButton('Коды ошибок '),
                   types.KeyboardButton('Промывка головки'),
                   types.KeyboardButton('Профилактика СНПЧ'),
                   types.KeyboardButton('Не сработал ключ InkWic'),
                   types.KeyboardButton('Адреса и время работы СЦ'),
                   types.KeyboardButton('Отправка в СЦ'),
                   ]
        markup.add(*buttons)
        bot.send_message(message.chat.id,
                         f'🚀*Привет. Я InkSystem Bot. Я могу:*\n\n'
                         f'1⃣ Показать текущий статус ремонта заказ-наряда\n\n'
                         f'2⃣ Показать расшифровку ошибок на печатающих устройствах Epson\n\n'
                         f'3⃣ Подсказать, как промыть печатающую головку\n\n'
                         f'4⃣ Подсказать, как провести профилактику картридже СНПЧ\n\n'
                         f'5⃣ Подсказать, что делать, если не сработал ключ InkWic\n\n'
                         f'6⃣ Подсказать адреса и время работы сервисных центров\n\n'
                         f'7⃣ Подсказать, как отправить печатающее устройство в сервисный центр\n\n',
                         reply_markup=markup,
                         parse_mode='Markdown')

    @bot.message_handler(content_types=['text'])
    def message_reply(message):

        if message.text == "Статус ремонта":
            response = 'Отправьте номер заказ-наряда в сообщении'

        elif message.text == 'Коды ошибок':
            response = give_data_from_file('errors_code')

        elif message.text == 'Промывка головки':
            response = give_data_from_file('flushing_print_head')

        elif message.text == 'Профилактика СНПЧ':
            response = give_data_from_file('prevention_CISS')

        elif message.text == 'Не сработал ключ InkWic':
            response = give_data_from_file('key_inkwic')

        elif message.text == 'Адреса и время работы СЦ':
            response = give_data_from_file('adresses_service_centers')

        elif message.text == 'Отправка в СЦ':
            response = give_data_from_file('send_service_center')

        elif message.text.isnumeric() and len(message.text) == 7:
            response = parse_data_from_site(message.text)

        else:
            response = 'Я не знаю такой команды :('

        bot.send_message(message.chat.id, response)

    bot.infinity_polling(none_stop=True, interval=0)


def main():
    token = os.getenv('API_BOT')
    telegram_bot(token)


if __name__ == '__main__':
    main()
