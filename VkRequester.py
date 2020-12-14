import os
import os.path as op
from itertools import chain
from pprint import pprint
from keys.config import CONFIG

import requests
from time import sleep


class VkUser:
    """Represents entity vk user"""

    url = 'https://api.vk.com/method/'
    TOKEN_PATH = 'keys/config.py'

    # todo:  Если токен отсутвует в конфиг файле или истек - сделать запрос на получения токена
    def __init__(self, uid=None, token=None ,version='5.126'):
        sleep(1)

        if token:
            CONFIG['token'] = token

        self.__token = CONFIG['token']
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
        # todo: Почему-то на некоторые ошибки VkApi приходит
        #  ответ с статус кодом 200
        response.raise_for_status()

        info: dict = response.json()

        if 'error' in info.keys():
            error = info['error']
            if error['error_code'] == 5:
                

        pprint(response.json())
        info = response.json()['response'][0]

        self.id = info['id']
        self.screen_name = info['screen_name']

    def __str__(self):
        uid = self.screen_name or 'id' + self.id
        return f'https://vk.com/{uid}'

    # todo было бы неплохо сделать поулчение общих друзей
    #  для нескольких пользователей как (user1 & user2 & ... & usern)
    def __and__(self, user):

        if not isinstance(user, VkUser):
            raise TypeError
        else:
            friends_url = self.url + 'friends.getMutual'
            friends_params = {
                'source_uid': self.id,
                'target_uid': user.id
            }

            response = requests.get(
                url=friends_url,
                params={**self.params, **friends_params}
            )
            response.raise_for_status()

            friends_ids = response.json()['response']
            friends = [VkUser(uid=id) for id in friends_ids]

            return friends

    def __get_token(self):
        path = op.join(os.getcwd(), self.TOKEN_PATH)
        try:
            with open(path, 'r') as f:
                token = f.readline()
        except FileNotFoundError:
            print("File not found")
        return token


if __name__ == '__main__':
    VkUser.TOKEN_PATH = 'keys/config.py'
    my_profile = VkUser()
    print(my_profile)
    another_user = VkUser(uid='40187990')
    print(another_user)
    friends = another_user & my_profile
    print(*friends, sep='\n')


