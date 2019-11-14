import base64, json, requests

__author__ = 'gmongalo'

SPOTIFY_URI_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URI_TOKEN = 'https:.//accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''


def getAuth(clientId, redirectURI, scope):
    data = f'{SPOTIFY_URI_AUTH}client_id={clientId}&response_type=code' \
           f'&redirect_uri={redirectURI}&scope={scope}'
    return data


def getToken(code, clientId, clientSecret, redirectURI):
    body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirectURI,
        'client_id': clientId,
        'client_secret': clientSecret
    }

    encoded = base64.b64encode(f'{clientId}:{clientSecret}')
    headers = {f'''Content-Type : HEADER, Authorization : Basic {encoded}'''}

    post = requests.post(SPOTIFY_URI_TOKEN, params=body, headers=headers)
    return handleToken(json.loads(post.text))


def handleToken(response):
    auth_head = {f'''Authorization: Bearer {response['access_token']}'''}
    REFRESH_TOKEN = response['response_token']
    return [response['access_token'], auth_head, response['scope'], response['expires_in']]

def refreshAuth():
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }

    postRefresh = requests.post(SPOTIFY_URI_TOKEN, data=body, headers=HEADER)
    pBack = json.dumps(postRefresh.text)

    return handleToken(pBack)
