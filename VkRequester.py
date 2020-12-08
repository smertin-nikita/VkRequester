import os
import os.path as op

import requests
from pprint import pprint


def get_token(path):
    try:
        with open(path, 'r') as f:
            token = f.readline()
    except FileNotFoundError:
        print("File not found")
    return token


class MyProfile:
    """Represents entity vk user"""

    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.__token = token
        self.version = version
        self.params = {
            'access_token': self.__token,
            'v': self.version
        }

        response = requests.get(
            url=self.url+'users.get',
            params={
                **self.params,
                'fields': 'screen_name'
            }
        )
        response.raise_for_status()
        info = response.json()
        self.id = info['response'][0]['id']
        self.screen_name = info['response'][0]['screen_name']

    def __str__(self):
        id = self.screen_name or 'id' + self.id
        return f'https://vk.com/{id}'

    def __and__(self, target_uid):
        friends_url = self.url + 'friends.getMutual'
        friends_params = {
            'source_uid': self.id,
            'target_uid': target_uid
        }
        res = requests.get(
            url=friends_url,
            params={**self.params, **friends_params}
        )
        return res.json()


if __name__ == '__main__':
    token_path = get_token(op.join(os.getcwd(), 'keys/token'))
    my_profile = MyProfile(token_path, '5.126')
    friends = my_profile.get_mutual('40187990')
    print(friends)


