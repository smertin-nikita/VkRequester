import requests

CONFIG = {
    'app_id': '7697314',
    'token': '',
    'v': '5.126',
    # But it is also an OAuth 2.0 provider and it needs scope.
    'scope': ['friends', 'photos']
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
