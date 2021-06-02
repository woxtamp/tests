class BaseSelenium:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://passport.yandex.ru/auth"

    def find_el_by_name(self, name):
        return self.driver.find_element_by_name(name)

    def find_el_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def go_to_site(self):
        return self.driver.get(self.base_url)

    def get_url(self):
        return self.driver.current_url
