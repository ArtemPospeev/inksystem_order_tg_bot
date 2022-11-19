from pathlib import Path
from loguru import logger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# emoji
emoji_order_number = '⚒'
emoji_start_date = '📆'
emoji_order_status = '📍'
emoji_device_name = '🔧'
emoji_breakdown_desc = '🔨'
emoji_appearance = '🎨'

emoji_list = [
    emoji_order_number,
    emoji_start_date,
    emoji_order_status,
    emoji_device_name,
    emoji_breakdown_desc,
    emoji_appearance,
]

# url
URL = 'http://remontprinterov.com/servis'

# init logger
logger.add("debug.log", format='{time} {level} {message', level='DEBUG')


def add_emoji(emoji: str, other_data: str) -> str:
    '''
    Добавляет эмоджи в начало строки
    :param emoji:str
    :param other_data:str
    :return str
    '''
    return f'{emoji} {other_data}'


def get_data_from_xpath(driver: webdriver, xpath: str) -> str:
    '''
    Возвращает элемент со страницы по xpath'у \n
    :param driver:webdriver \n
    :param xpath:str \n
    :return str
    '''
    return f'{driver.find_element("xpath", f"{xpath}").text}'


def make_beautiful_answer(*args) -> str:
    '''
    Собирает строки в красивый ответ \n
    :arg str, str, str \n
    :return str
    '''
    res = ''
    for emoji, el in zip(emoji_list, args):
        res += f'{emoji} {el} \n'
    return res


def init_browser(headless: bool = True) -> webdriver:
    '''
    Инициализирует браузер с опциями, возвращает driver \n
    :param headless= Bool \n
    :return selenium.driver
    '''
    logger.info(' Отправляен запрос на сайт ')

    # web driver options
    options = webdriver.ChromeOptions()

    # headless mode
    if headless:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    # driver
    path_to_driver = str(Path(__file__).parent / 'chromedriver/chromedriver')
    driver = webdriver.Chrome(
        service=Service(path_to_driver),
        options=options,
    )
    return driver


def parse_data_from_site(order_number: str | int, url: str = URL) -> str:
    driver = init_browser()

    try:  # Отливливаем исключения при поиске элементов
        driver.get(url=url)

        order_input = driver.find_element('name', 'number_zakaz')  # Ищем элемент на странице по имени
        order_input.clear()  # На всякий случай очищаем поле ввода
        order_input.send_keys(str(order_number))  # Вставляем туда принятый номер заказ - наряда
        order_input.send_keys(Keys.ENTER)  # Отправляем запрос (через нажатие Enter)

        # Ниже парсим по XPath все нужные столбцы таблицы
        order_number = get_data_from_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[1]")

        start_date = get_data_from_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[2]")

        order_status = get_data_from_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[3]")

        device_name = get_data_from_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[5]")

        breakdown_desc = get_data_from_xpath(driver, '/html/body/div[1]/section/div/div/div/table/tbody/tr[7]')

        appearance = get_data_from_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[8]")

        # Собираем ответ
        data = make_beautiful_answer(
            order_number,
            start_date,
            order_status,
            device_name,
            breakdown_desc,
            appearance,
        )

    except NoSuchElementException:  # Не нашли элемент на странице (скорее всего упал сайт)
        data = 'Проблемы с доступом к базе данных. Попробуйте позже'
        logger.error('Не удалось отправить запрос на сайт/ не удалось распарсить элементы')

    except Exception as err:  # На всякий случай ловим всем остальные ошибки.
        logger.error(f'{err}\n')
        data = f'Произошла ошибка, пожалуйста, сделайте скрин и сообщите о ней сотрудникам компании'

    finally:
        driver.close()
        driver.quit()

    logger.info('Данные с сайта успешно получены')
    return data


if __name__ == '__main__':
    print(parse_data_from_site(2201020))
