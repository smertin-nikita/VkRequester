import os
import os.path as op
from pprint import pprint
from config import CONFIG, get_url_for_token

import requests
from time import sleep


class VkUser:
    """Represents entity vk user"""

    url = 'https://api.vk.com/method/'

    def __init__(self, uid=None, token=None, version='5.126'):
        sleep(1)

        if token:
            CONFIG['token'] = token

        if not CONFIG['token']:
            raise Exception(get_url_for_token())

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

        response.raise_for_status()

        info: dict = response.json()

        if 'error' in info.keys():
            raise Exception(info['error'])

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
            info: dict = response.json()
            if 'error' in info.keys():
                raise Exception(info['error'])

            friends_ids = response.json()['response']
            friends = [VkUser(uid=id) for id in friends_ids]

            return friends

    def get_photos(self, likes=None, album_id='profile'):
        """Returns photos by number of likes"""

        params = {
            'owner_id': self.id,
            'album_id': album_id,
            'extended': 1,
            'count': 200,
            'skip_hidden': 1
        }

        response = requests.get(
            url=self.url + 'photos.get',
            params={**self.params, **params}

        )
        response.raise_for_status()
        info: dict = response.json()
        if 'error' in info.keys():
            raise Exception(info['error'])

        photos = info['response']['items']
        if likes:
            most_likes = [photo for photo in photos if photo['likes']['count'] >= likes]
            return most_likes
        else:
            return photos


    # def __get_token(self):
    #     path = op.join(os.getcwd(), self.TOKEN_PATH)
    #     try:
    #         with open(path, 'r') as f:
    #             token = f.readline()
    #     except FileNotFoundError:
    #         print("File not found")
    #     return token


if __name__ == '__main__':
    # print(get_url_for_token())
    another_user = VkUser('begemot_korovin')
    print(another_user)
    pprint(another_user.get_photos(1))


