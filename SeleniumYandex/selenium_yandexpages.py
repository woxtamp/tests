from base_selenium import BaseSelenium


class Elements:
    LOGIN_FIELD_NAME = 'login'
    PASSWORD_FIELD_NAME = 'passwd'
    LOGIN_BUTTON_XPATH = "//body/div[@id='root']/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[" \
                         "1]/div[1]/form[1]/div[3]/button[1]"
    LOGIN_INVALID_XPATH = "//div[contains(text(), 'Такой логин не подойдет')]"
    LOGIN_NO_XPATH = "//div[contains(text(), 'Логин не указан')]"
    LOGIN_NON_EXIST_XPATH = "//div[contains(text(), 'Такого аккаунта нет')]"
    PASSWORD_INVALID = "//div[contains(text(), 'Неверный пароль')]"
    AUTHORIZE_BUTTON_XPATH = "//body/div[@id='root']/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[" \
                             "1]/div[1]/form[1]/div[3]/button[1] "
    AUTHORIZED_TEXT = "//a[contains(text(),'Управление аккаунтом')]"


class SeleniumHelper(BaseSelenium):

    def enter_login(self, login):
        login_field = self.find_el_by_name(Elements.LOGIN_FIELD_NAME)
        login_field.send_keys(login)

    def click_to_login_button(self):
        button = self.find_el_by_xpath(Elements.LOGIN_BUTTON_XPATH)
        button.click()

    def find_invalid_login_message(self):
        return self.find_el_by_xpath(Elements.LOGIN_INVALID_XPATH)

    def find_no_login_message(self):
        return self.find_el_by_xpath(Elements.LOGIN_NO_XPATH)

    def find_non_exist_message(self):
        return self.find_el_by_xpath(Elements.LOGIN_NON_EXIST_XPATH)

    def find_password_field(self):
        return self.find_el_by_name(Elements.PASSWORD_FIELD_NAME)

    def enter_password(self, password):
        password_field = self.find_el_by_name(Elements.PASSWORD_FIELD_NAME)
        password_field.send_keys(password)

    def click_to_authorize_button(self):
        button = self.find_el_by_xpath(Elements.AUTHORIZE_BUTTON_XPATH)
        button.click()

    def find_invalid_password_message(self):
        return self.find_el_by_xpath(Elements.PASSWORD_INVALID)

    def find_authorized_text(self):
        return self.find_el_by_xpath(Elements.AUTHORIZED_TEXT)

    # def enter_word(self, word):
    #     search_field = self.find_element(YandexSeacrhLocators.LOCATOR_YANDEX_SEARCH_FIELD)
    #     search_field.click()
    #     search_field.send_keys(word)
    #     return search_field
    #
    # def click_on_the_search_button(self):
    #     return self.find_element(YandexSeacrhLocators.LOCATOR_YANDEX_SEARCH_BUTTON, time=2).click()
    #
    # def check_navigation_bar(self):
    #     all_list = self.find_elements(YandexSeacrhLocators.LOCATOR_YANDEX_NAVIGATION_BAR, time=2)
    #     nav_bar_menu = [x.text for x in all_list if len(x.text) > 0]
    #     return nav_bar_menu
