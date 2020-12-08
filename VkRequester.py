import requests
from pprint import pprint


class VkUser:
    """Represents entity vk user"""

    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.__token = token
        self.version = version
        self.params = {
            'access_token': self.__token,
            'v': self.version
        }
        info = requests.get(
            url=self.url+'users.get',
            params={
                **self.params,
                'fields': 'screen_name'
            }
        ).json()
        self.id = info['response'][0]['id']
        self.screen_name = info['response'][0]['screen_name']

    def __str__(self):
        id = self.screen_name or self.id
        return f'https://vk.com/{id}'


if __name__ == '__main__':
    vk_user = VkUser('10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c', '5.126')
    print(vk_user)
