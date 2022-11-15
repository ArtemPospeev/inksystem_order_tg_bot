from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent


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
        executable_path='/home/master/Documents/github/inksystem_order_tg_bot/chromedriver/chromedriver',
        options=options,
    )

    try:
        driver.get(url=url)

        order_input = driver.find_element('name', 'number_zakaz')
        order_input.clear()
        order_input.send_keys(str(order_number))
        order_input.send_keys(Keys.ENTER)

        data = driver.find_element('tag name', 'tbody').text

    except NoSuchElementException:
        data = 'Неверный номер заказ-наряда. Попробуйте ещё раз'

    except Exception as err:
        print(err)
        data = f'{err}\nПроизошла ошибка, пожалуйста, сообщите о ней сотрудникам компании'

    finally:
        driver.close()
        driver.quit()

    return data
