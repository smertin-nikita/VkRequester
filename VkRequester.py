import os
import os.path as op
from pprint import pprint

import requests
from time import sleep


CONFIG = {
    'app_id': '7697314',
    'token': '',
    'v': '5.126',
    # But it is also an OAuth 2.0 provider and it needs scope.
    'scope': ['photos']
}


def get_url_for_token():
    return requests.get(
        url='https://oauth.vk.com/authorize',
        params={
            'client_id': CONFIG['app_id'],
            'display': 'page',
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'scope': CONFIG['scope'],
            'response_type': 'token',
            'v': CONFIG['v']
        }
    ).url


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
        """Return photos by number of likes"""

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
