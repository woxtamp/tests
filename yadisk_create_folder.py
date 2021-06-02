import requests


class YaDiskCreateFolder:
    def __init__(self, token):
        self.token = token
        if self.token == '':
            print('Ошибка! Не указан токен!')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self):
        ya_disk_folder = input('Введите имя папки: ')
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': ya_disk_folder}
        response = requests.put(upload_url, headers=headers, params=params)
        return response.status_code, response.json()
