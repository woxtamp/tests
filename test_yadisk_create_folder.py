import yadisk_create_folder
import os
from dotenv import load_dotenv
import time
import datetime
import requests
import unittest.mock as mock
import allure

# Проверяем наличие файла .env и если он существует, то выгружаем оттуда данные
dotenv_path = os.path.join('.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

YANDEX_DISK_TOKEN = os.getenv('YANDEX_DISK_TOKEN')
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
HEADERS = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(YANDEX_DISK_TOKEN)
}


class TestYaDiskCreateFolder:

    @allure.feature('Яндекс.Диск')
    @allure.story('Создание новой папки - ожидаем ответ с кодом 201')
    def test_create_new_folder(self):
        folder_name = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        folder_replaced = folder_name.replace(' ', '+')
        with mock.patch('yadisk_create_folder.input', return_value=folder_name):
            with allure.step('Проверим, что папка создалась на диске'):
                assert yadisk_create_folder.YaDiskCreateFolder(YANDEX_DISK_TOKEN).create_folder() == (
                    201, {'href': f'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{folder_replaced}',
                          'method': 'GET', 'templated': False})
        with allure.step('Удалим созданную папку'):
            url = URL
            headers = HEADERS
            params = {'path': folder_name}
            requests.delete(url, headers=headers, params=params)

    @allure.feature('Яндекс.Диск')
    @allure.story('Попытка создания папки с уже существующим именем - ожидаем ответ с кодом 409')
    def test_create_exist_folder(self):
        folder_name = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        folder_replaced = folder_name.replace(' ', '+')
        with mock.patch('yadisk_create_folder.input', return_value=folder_name):
            with allure.step('Проверим, что папка создалась на диске'):
                assert yadisk_create_folder.YaDiskCreateFolder(YANDEX_DISK_TOKEN).create_folder() == (
                    201, {'href': f'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{folder_replaced}',
                          'method': 'GET', 'templated': False})
        with mock.patch('yadisk_create_folder.input', return_value=folder_name):
            with allure.step('Проверим, что папка не создалась на диске'):
                assert yadisk_create_folder.YaDiskCreateFolder(YANDEX_DISK_TOKEN).create_folder() == (
                    409, {'message': f'По указанному пути \"{folder_name}\" уже существует папка с таким именем.',
                          'description': f'Specified path \"{folder_name}\" points to existent directory.',
                          'error': 'DiskPathPointsToExistentDirectoryError'})
        with allure.step('Удалим созданную папку'):
            url = URL
            headers = HEADERS
            params = {'path': folder_name}
            requests.delete(url, headers=headers, params=params)

    @allure.feature('Яндекс.Диск')
    @allure.story('Попытка создания папки без авторизации - ожидаем ответ с кодом 401')
    def test_create_folder_unauthorized(self):
        folder_name = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        with mock.patch('yadisk_create_folder.input', return_value=folder_name):
            with allure.step('Проверим, что папка создалась на диске'):
                assert yadisk_create_folder.YaDiskCreateFolder('').create_folder() == (
                    401, {'message': 'Не авторизован.', 'description': 'Unauthorized', 'error': 'UnauthorizedError'})

    @allure.feature('Яндекс.Диск')
    @allure.story('Попытка создания папки без указания имени - ожидаем ответ с кодом 400')
    def test_create_folder_with_no_name(self):
        with mock.patch('yadisk_create_folder.input', return_value=''):
            with allure.step('Проверим, что папка создалась на диске'):
                assert yadisk_create_folder.YaDiskCreateFolder(YANDEX_DISK_TOKEN).create_folder() == (
                    400, {'message': 'Ошибка проверки поля "path": Это поле является обязательным.',
                          'description': 'Error validating field "path": This field is required.',
                          'error': 'FieldValidationError'})
