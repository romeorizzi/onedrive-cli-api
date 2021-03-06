import pprint
import base64
import mimetypes
import os
import urllib
import sys
import webbrowser
import math
from adal import AuthenticationContext
import pyperclip
import requests
import json
import os.path
from os import path
from datetime import datetime

CLIENT_ID = 'CLIENT-CODE-HERE'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'beta'
TOKEN_PATH = 'token.json'


def api_endpoint(url):
    if urllib.parse.urlparse(url).scheme in ['http', 'https']:
        return url  # url is already complete
    return urllib.parse.urljoin(f'{RESOURCE}/{API_VERSION}/', url.lstrip('/'))


def expired(date_str):
    exp_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
    current = datetime.now()
    time_delta = exp_date - current
    if time_delta.total_seconds() > 0:
        return False
    else:
        return True


def first_time(ctx, device_code):
    pyperclip.copy(device_code['user_code'])  # copy user code to clipboard
    webbrowser.open(device_code['verification_url'])  # open browser
    print(f'The code {device_code["user_code"]} has been copied to your clipboard, '
          f'and your web browser is opening {device_code["verification_url"]}. '
          'Paste the code to sign in.')
    token_response = ctx.acquire_token_with_device_code(RESOURCE, device_code, CLIENT_ID)
    with open("token.json", 'w') as f:
        json.dump(token_response, f)
    return token_response["accessToken"]


def device_flow_session(client_id=CLIENT_ID, auto=False):
    ctx = AuthenticationContext(AUTHORITY_URL, api_version=None)
    device_code = ctx.acquire_user_code(RESOURCE, client_id)
    if path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            token_info = json.load(f)
        if not expired(token_info['expiresOn']):
            print("You're already logged in")
            token = token_info['accessToken']
        else:
            print("Expired token")
            token = first_time(ctx, device_code)
    else:
        token = first_time(ctx, device_code)

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {token}',
                            'SdkVersion': 'sample-python-adal',
                            'x-client-SKU': 'sample-python-adal'})
    return session
