"""Python console app with device flow authentication."""
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.

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

from data_for_user_customization import CLIENT_ID, TENANT_ID

AUTHORITY_URL = 'https://login.microsoftonline.com/' + TENANT_ID 

print(f"TENANT_ID: {TENANT_ID}")
print(f"CLIENT_ID: {CLIENT_ID}")
print(f"AUTHORITY_URL: {AUTHORITY_URL}")

RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'beta'


def api_endpoint(url):
    if urllib.parse.urlparse(url).scheme in ['http', 'https']:
        return url  
    return urllib.parse.urljoin(f'{RESOURCE}/{API_VERSION}/',
                                url.lstrip('/'))


def device_flow_session(client_id, auto=True):
    ctx = AuthenticationContext(AUTHORITY_URL, api_version=None)
    device_code = ctx.acquire_user_code(RESOURCE, client_id)

    # display user instructions
    if auto: # giro user_code e verification_url all'utente che ha un tempo limitato per autenticarsi
        pyperclip.copy(device_code['user_code'])  # copy user code to clipboard
        webbrowser.open(device_code['verification_url'])  # open browser
        print(f'The code {device_code["user_code"]} has been copied to your clipboard, '
              f'and your web browser is opening {device_code["verification_url"]}. '
              'Paste the code to sign in.')
    else:
        print(device_code['message'])

    # dopo che l'utente si è autenticato, si può "acquisire" il token "scambiandolo" con il device_code

    token_response = ctx.acquire_token_with_device_code(RESOURCE, device_code, client_id)
    if not token_response.get('accessToken', None):
        return None

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {token_response["accessToken"]}',
                            'SdkVersion': 'sample-python-adal',
                            'x-client-SKU': 'sample-python-adal'})
    return session


def get_item_id(session, item_path):
    fname_only = os.path.basename(item_path)
    print(f'Getting id of {fname_only}')
    endpoint = f'/me/drive/root:/{item_path}'
    response = session.get(api_endpoint(endpoint)) # response contiene info sulla pagina (docum) aperto dall'url in input
    print(response)
    #print('json', response.json())
    return response.json()['id']


def invite_student(session, item_id, student_mail, permission): # item_id is response.json()['id']
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


if __name__ == '__main__':
    
########################## INIZIO INPUT ##############################
# Per utilizzare il codice modificate questi parametri (o inseriteli da terminale come argv[])
    if len(sys.argv) == 1:
        print(f"Usage:\n   {sys.argv[0]} rel_path_of_file_from_root student_mail (r|w)")
        sys.exit()
    item_path = sys.argv[1]
    student_mail = sys.argv[2]
    if sys.argv[3] == 'r':
        permission = "read"
    elif sys.argv[3] == 'w':
        permission = "write"
    
    ######TEST INFO######
    #Alternativamente, se non si vuole inserire da terminale.
    """
    item_path = 'fascicolo2.pdf'
    student_mail = 'davide.roznowicz@gmail.com'
    permission = 'read'
    """
########################## FINE INPUT ##############################   
    
    
    GRAPH_SESSION = device_flow_session(CLIENT_ID)
    if GRAPH_SESSION: # if None --> False
        item_id = get_item_id(GRAPH_SESSION, item_path) # esempio: item_id='01GJ5S5QPJL4RWEX72O5A2VCU2GGMS6UVZ'
        print(invite_student(GRAPH_SESSION, item_id, student_mail, permission))
