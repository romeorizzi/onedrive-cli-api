#!/usr/bin/python3
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


def device_flow_session(client_id, auto=False):
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


def get_item_id(session, item_path):
    fname_only = os.path.basename(item_path)
    print(f'Getting id of {fname_only}')
    endpoint = f'/me/drive/root:/{item_path}'
    response = session.get(api_endpoint(endpoint))
    print(response)
    return response.json()['id']


def invite_student(session, item_id, student_mail, permission):
    print(f'Inviting {student_mail} with {permission} permission')
    endpoint = f'/me/drive/items/{item_id}/invite'
    response = session.post(api_endpoint(endpoint),
                            headers={'Content-Type': 'application/json'},
                            json={"recipients": [{"email": student_mail}],
                                  "message": "Here's the file that we're collaborating on.", "requireSignIn": True,
                                  "sendInvitation": True, "roles": [permission]})
    if response.ok:
        # status 201 = link created, status 200 = existing link returned
        return (response)
    return (response)


if len(sys.argv) != 4:
    print("Usage: ./share.py file_path student_mail -r|-w")
    print("Example: ./share.py esamiRO/2020-07-27/id076596 id076596@studenti.univr.it -r")
    sys.exit()

item_path = sys.argv[1]
student_mail = sys.argv[2]
if sys.argv[3] == '-r':
    permission = "read"
elif sys.argv[3] == '-w':
    permission = "write"

GRAPH_SESSION = device_flow_session(CLIENT_ID)
if GRAPH_SESSION:
    item_id = get_item_id(GRAPH_SESSION, item_path)
    print(invite_student(GRAPH_SESSION,item_id,student_mail,permission))
