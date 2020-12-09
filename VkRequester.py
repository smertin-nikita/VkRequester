import os
import os.path as op

import requests
from pprint import pprint


class VkUser:
    """Represents entity vk user"""

    url = 'https://api.vk.com/method/'

    # todo:  Если токен отсутвует в конфиг файле или истек - сделать запрос на получения токена
    def __init__(self, version='5.126', uid=None):
        self.__token = self.__get_token()
        self.version = version
        self.params = {
            'access_token': self.__token,
            'v': self.version
        }

        # todo: Пока жестко закодированы. Либо расшрить поля,
        #  либо добавлять списком или словарем как параметр или иначе...
        fields = ['screen_name']

        response = requests.get(
            url=self.url+'users.get',
            params={
                **self.params,
                'user_ids': uid,
                'fields': fields
            }
        )
        # todo: Почему-то не отлвливает ошибки VkApi
        response.raise_for_status()

        print(response.json())
        info = response.json()['response'][0]

        self.id = info['id']
        self.screen_name = info['screen_name']

    def __str__(self):
        uid = self.screen_name or 'id' + self.id
        return f'https://vk.com/{uid}'

    def __and__(self, target_uid):
        friends_url = self.url + 'friends.getMutual'
        friends_params = {
            'source_uid': self.id,
            'target_uid': target_uid
        }

        response = requests.get(
            url=friends_url,
            params={**self.params, **friends_params}
        )
        response.raise_for_status()
        return response.json()

    TOKEN_PATH = 'keys/token'

    def __get_token(self):
        path = op.join(os.getcwd(), self.TOKEN_PATH)
        try:
            with open(path, 'r') as f:
                token = f.readline()
        except FileNotFoundError:
            print("File not found")
        return token


if __name__ == '__main__':
    my_profile = VkUser()
    print(my_profile)
    another_user = VkUser(uid='40187990')
    print(another_user)
    # friends = my_profile.get_mutual('40187990')
    # print(friends)


