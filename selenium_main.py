from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent

# emoji
emoji_order_number = '⚒'
emoji_start_date = '📆'
emoji_order_status = '📍'
emoji_device_name = '🔧'
emoji_breakdown_desc = '🔨'
emoji_appearance = '🎨'


def add_emoji(emoji: str, other_data: str) -> str:
    ''' Добавляет эмоджи в начало строки'''
    return f'{emoji} {other_data}'


def get_data_with_xpath(driver, xpath):
    ''' Возвращает элемент со страницы'''
    return f'{driver.find_element("xpath", f"{xpath}").text}'


def make_beautiful_answer(*args):
    ''' Собирает строки в красивый ответ '''
    return '\n'.join(*args)


def parse_data_from_site(order_number):
    # user agent
    user_agent = UserAgent()

    # options
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent.opera}')

    # headless mode
    options.add_argument('--headless')

    # Url + driver
    url = 'http://remontprinterov.com/servis'
    driver = webdriver.Chrome(
        executable_path=Path(__file__).parent / 'chromedriver/chromedriver',
        options=options,
    )

    try:
        driver.get(url=url)

        order_input = driver.find_element('name', 'number_zakaz')
        order_input.clear()
        order_input.send_keys(str(order_number))
        order_input.send_keys(Keys.ENTER)

        order_number = add_emoji(emoji_order_number,
                                 get_data_with_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[1]")
                                 )

        start_date = add_emoji(emoji_start_date,
                               get_data_with_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[2]")
                               )

        order_status = add_emoji(emoji_order_status,
                                 get_data_with_xpath(driver,
                                                     "/html/body/div[1]/section/div/div/div/table/tbody/tr[3]"))

        device_name = add_emoji(emoji_device_name,
                                get_data_with_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[5]")
                                )

        breakdown_desc = add_emoji(emoji_breakdown_desc,
                                   get_data_with_xpath(driver,
                                                       '/html/body/div[1]/section/div/div/div/table/tbody/tr[7]')
                                   )

        appearance = add_emoji(emoji_appearance,
                               get_data_with_xpath(driver, "/html/body/div[1]/section/div/div/div/table/tbody/tr[8]")
                               )

        data = make_beautiful_answer(
            order_number,
            start_date,
            order_status,
            device_name,
            breakdown_desc,
            appearance,
        )
    except NoSuchElementException:
        data = 'Неверный номер заказ-наряда. Попробуйте ещё раз'

    except Exception as err:
        print(err)
        data = f'{err}\nПроизошла ошибка, пожалуйста, сообщите о ней сотрудникам компании'

    finally:
        driver.close()
        driver.quit()

    return data


if __name__ == '__main__':
    print(parse_data_from_site(2201020))
