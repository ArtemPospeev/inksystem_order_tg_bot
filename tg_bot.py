import os
from pathlib import Path
from dotenv import load_dotenv

from telebot import types, telebot
from loguru import logger

from selenium_main import parse_data_from_site

# load environment variables
BASE_DIR = Path(__file__).resolve().parent
FILE_DIR = BASE_DIR / 'files_ru/'
CODING = 'UTF-8'
dot_env = BASE_DIR / '.env'
load_dotenv(dotenv_path=dot_env)

# init logger
logger.add("debug.log", format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')

greeting = f'🚀 *Привет. Я InkSystem Bot. Я могу:*\n\n' \
           f'1⃣ Показать текущий статус ремонта заказ-наряда\n\n' \
           f'2⃣ Показать расшифровку ошибок на печатающих устройствах Epson\n\n' \
           f'3⃣ Подсказать, как промыть печатающую головку\n\n' \
           f'4⃣ Подсказать, как провести профилактику картриджей СНПЧ (удалить воздух)\n\n' \
           f'5⃣ Подсказать, что делать, если не сработал ключ InkWic\n\n' \
           f'6⃣ Подсказать адреса и время работы сервисных центров\n\n' \
           f'7⃣ Подсказать, как отправить печатающее устройство в сервисный центр\n\n' \
           f'8⃣ Подсказать, как убрать уведомление об обновлении ПО\n\n' \
           f'9⃣ Подсказать, как проверить, правильно ли установлены картриджи\n\n' \
           f'1⃣0⃣ Подсказать, где оставить заявку на сервисное/удаленное/дистанционное обслуживание\n\n'


@logger.catch
def give_data_from_file(file: str) -> str:
    '''
    Возвращает содержимое файла
    :param file: str - путь до файла
    :return str - содержимое файла
    '''
    with open(FILE_DIR / (file + '.txt'), 'r', encoding=CODING) as f:
        text = f.read()
    return text


@logger.catch
def search_in_file(search_object: str, file: str = './files_ru/errors_code.txt') -> str:
    '''
    Ищет по номеру ошибки её описание в файле, возвращает текст ошибки
    :param search_object: str - объект поиска
    :param file: str - путь до файла
    :return:
    '''
    with open(file, 'r') as f:
        for line in f.readlines():
            if search_object in line:
                return line

    return 'Не найдено такой ошибки'


@logger.catch
def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'info'])  # Обработка команды старт
    def start_message(message):
        logger.info(f'Новое обращение к боту от пользователя')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Инициализируем клавиатуру
        buttons = [types.KeyboardButton('Статус ремонта'),  # Кнопки
                   types.KeyboardButton('Коды ошибок'),
                   types.KeyboardButton('Промывка головки'),
                   types.KeyboardButton('Воздух в шлейфе СНПЧ'),
                   types.KeyboardButton('Установка картр. СНПЧ'),
                   types.KeyboardButton('Уведомление об обн. ПО'),
                   types.KeyboardButton('Не сработал ключ InkWic'),
                   types.KeyboardButton('Адреса и время работы СЦ'),
                   types.KeyboardButton('Отправка в СЦ'),
                   types.KeyboardButton('Заявки в СЦ'),
                   ]
        markup.add(*buttons)
        bot.send_message(message.chat.id,  # Отправка сообщения после /start
                         greeting,
                         reply_markup=markup,
                         parse_mode='Markdown')

    @bot.message_handler(content_types=['text'])  # Обработка входящего сообщения от пользователя
    def message_reply(message):
        # Сначала обрабатываем все кнопки (если к нам пришел от пользователя текст):
        if message.text == "Статус ремонта":
            response = 'Отправьте номер заказ-наряда в сообщении'

        elif message.text == 'Коды ошибок':
            response = 'Отправьте номер ошибки в чат (формат: 000031, 0x01, 0x62, 0x9a, 0xF4 и т.д.)'

        elif message.text == 'Промывка головки':
            response = give_data_from_file('flushing_print_head')

        elif message.text == 'Воздух в шлейфе СНПЧ':
            response = give_data_from_file('prevention_CISS')

        elif message.text == 'Уведомление об обн. ПО':
            response = give_data_from_file('firmware_update_notification')

        elif message.text == 'Установка картр. СНПЧ':
            response = give_data_from_file('cartridges_inserted_correctly')

        elif message.text == 'Не сработал ключ InkWic':
            response = give_data_from_file('key_inkwic')

        elif message.text == 'Адреса и время работы СЦ':
            response = give_data_from_file('adresses_service_centers')

        elif message.text == 'Отправка в СЦ':
            response = give_data_from_file('send_service_center')

        elif message.text == 'Заявки в СЦ':
            response = give_data_from_file('service_requests')

        # В этом блоке if проверяем, надо ли нам делать запрос к сайту (длина строки и состоит только из цифр)
        elif message.text.isnumeric() and message.text[0] == '2' and len(message.text) == 7:
            response = parse_data_from_site(message.text)

        # В этом блоке if проверяем, надо ли нам искать вхождение в файле с описанием ошибок
        elif 'x' in message.text or (message.text.isnumeric() and len(message.text) == 6):
            response = search_in_file(message.text)

        else:
            response = 'Я не знаю такой команды :('

        logger.info('Отправлен ответ пользователю')
        bot.send_message(message.chat.id, response)  # Отправка ответа пользователю.

    bot.infinity_polling(none_stop=True, interval=0)  # Бесконечный цикл для бота


def main():
    token = os.getenv('API_BOT')
    telegram_bot(token)


if __name__ == '__main__':
    main()
