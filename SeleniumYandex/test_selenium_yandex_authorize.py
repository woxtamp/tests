import time
import uuid
import allure
from selenium_yandexpages import SeleniumHelper

CHROMEDRIVER_PATH = r'C:\chromedriver.exe'


class TestSeleniumYandexAuthorize:

    @allure.feature('Яндекс.Паспорт')
    @allure.story('Попытка логина с некорректными данными')
    def test_authorize_non_valid(self, browser):
        page = SeleniumHelper(browser)
        page.go_to_site()
        page.enter_login(str(uuid.uuid4()))
        page.click_to_login_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователю показывается сообщение об ошибке'):
            assert page.find_invalid_login_message()

    @allure.feature('Яндекс.Паспорт')
    @allure.story('Попытка логина с пустыми данными')
    def test_authorize_empty(self, browser):
        page = SeleniumHelper(browser)
        page.go_to_site()
        page.enter_login('')
        page.click_to_login_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователю показывается сообщение об ошибке'):
            assert page.find_no_login_message()

    @allure.feature('Яндекс.Паспорт')
    @allure.story('Попытка логина с несуществующими данными')
    def test_authorize_non_exist(self, browser):
        page = SeleniumHelper(browser)
        page.go_to_site()
        page.enter_login('netology-python-qwerty-595')
        page.click_to_login_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователю показывается сообщение об ошибке'):
            assert page.find_non_exist_message()

    @allure.feature('Яндекс.Паспорт')
    @allure.story('Попытка логина с некорректным паролем')
    def test_authorize_wrong_pass(self, browser):
        page = SeleniumHelper(browser)
        page.go_to_site()
        page.enter_login('netology-python-qwerty-500')
        page.click_to_login_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователю стало доступно поле для ввода пароля'):
            assert page.find_password_field()
        page.enter_password('123456Qwerty11')
        page.click_to_authorize_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователю показывается сообщение об ошибке'):
            assert page.find_invalid_password_message()

    @allure.feature('Яндекс.Паспорт')
    @allure.story('Успешный логин')
    def test_authorize_complete(self, browser):
        page = SeleniumHelper(browser)
        page.go_to_site()
        page.enter_login('netology-python-qwerty-500')
        page.click_to_login_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователю стало доступно поле для ввода пароля'):
            assert page.find_password_field()
        page.enter_password('123456Qwerty')
        page.click_to_authorize_button()
        time.sleep(1)
        with allure.step('Проверим, что пользователь залогинился'):
            assert page.find_authorized_text()
            assert 'profile' in page.get_url()
