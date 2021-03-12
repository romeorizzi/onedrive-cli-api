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
import json
import os.path
from os import path
from datetime import datetime

from data_for_user_customization_template import CLIENT_ID, TENANT_ID

AUTHORITY_URL = 'https://login.microsoftonline.com/' + TENANT_ID 

print(f"TENANT_ID: {TENANT_ID}")
print(f"CLIENT_ID: {CLIENT_ID}")
print(f"AUTHORITY_URL: {AUTHORITY_URL}")

RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'beta'
TOKEN_PATH = 'token.json'




def api_endpoint(url):
    if urllib.parse.urlparse(url).scheme in ['http', 'https']:
        return url  
    return urllib.parse.urljoin(f'{RESOURCE}/{API_VERSION}/',
                                url.lstrip('/'))


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
    print(f'Getting id of {fname_only}...')
    endpoint = f'/me/drive/root:/{item_path}'
    response = session.get(api_endpoint(endpoint)) # response contiene info sulla pagina (docum) aperto dall'url in input
    print(response)
    #print('json', response.json())
    return response.json()




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
    
    
    
def print_current_permissions(response):
    print("\nPermissions granted to the following people (besides the owner):\n")
    for k in range(0,len(response.json()['value'])):
    # if the key grantedToIdentities is present for this specific k
         if response.json()['value'][k].get('grantedToIdentities'):
             for j in range(0,len(response.json()['value'][k]['grantedToIdentities'])):
                 email = response.json()['value'][k]['grantedToIdentities'][j]['user']['email']
                 perm_granted = response.json()['value'][k]['roles']
                 perm_id = response.json()['value'][k]['id']
                 print(f"mail: {email}\t      permission: {perm_granted}\t      perm-id: {perm_id}")



def check_permission(role):
    del_perm = "to_set"
    if permission == '-r':
        del_perm = "read"
    elif permission == '-w':
        del_perm = "write"

    return role == del_perm



def remove_student_permission(session, item_id, student_mail, permission):
    print(f'Getting perm-id for item shared with {student_mail}...')
    print(f'Removing permission ({permission}) to shared item from email {student_mail}...')
    endpoint = f'/me/drive/items/{item_id}/permissions'
    response = session.get(api_endpoint(endpoint))
    
    perm_id = False
    for k in range(0,len(response.json()['value'])):
    # if the key grantedToIdentities is present for this specific k
        if response.json()['value'][k].get('grantedToIdentities'):
            for j in range(0,len(response.json()['value'][k]['grantedToIdentities'])):
                if response.json()['value'][k]['grantedToIdentities'][j]['user']['email'] == student_mail and \
                			check_permission(response.json()['value'][k]['roles'][0]):
                    perm_id = response.json()['value'][k]['id']
                    break
    
    if perm_id == False:
        print("No permission was found according to your requests...\n") 
        print_current_permissions(response)
        return ""
    
    print("*********************************************\nBefore:")            
    print_current_permissions(response)
    endpoint2 = f'/me/drive/items/{item_id}/permissions/{perm_id}'
    response2 = session.delete(api_endpoint(endpoint2))
    print("\n\n\n\nAfter:")
    response3 = session.get(api_endpoint(endpoint))
    print_current_permissions(response3)
    print("*********************************************\n")
    
    return response
    
    
    
if len(sys.argv) != 4:
    print("Usage: share.py file_path student_mail -r|-w")
    print("Example: share.py esamiRO/2020-07-27/id076596 id076596@studenti.univr.it -r")
    sys.exit()

    
    
    
# Per utilizzare il codice modificate questi parametri (o inseriteli da terminale come argv[])
########################## INIZIO INPUT ##############################
if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        print("share.py rel_path_of_file_from_root student_mail r|w")
        sys.exit()
    item_path = sys.argv[1]
    student_mail = sys.argv[2]
    if sys.argv[3] == 'r':
        permission = "read"
    elif sys.argv[3] == 'w':
        permission = "write"
    else:
        if (sys.argv[3] in ['-r', '-w', 'del_all']): 
            permission = sys.argv[3]
        else:
            print("Not allowed permission! Please choose between w,r,-w,-r,del_all")
            sys.exit()

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
        item_id = get_item_id(GRAPH_SESSION, item_path)['id'] # esempio: item_id='01GJ5S5QPJL4RWEX72O5A2VCU2GGMS6UVZ'
        if permission not in ['-r', '-w', 'del_all']:
            print(invite_student(GRAPH_SESSION, item_id, student_mail, permission))
        else:  # in ['-r', '-w', 'del_all']
            if permission == 'del_all':
                permission = '-r'
                print(remove_student_permission(GRAPH_SESSION, item_id, student_mail, '-r'))
                permission = '-w'
                print(remove_student_permission(GRAPH_SESSION, item_id, student_mail, '-w'))
            else:  # in ['-r', '-w']
                print(remove_student_permission(GRAPH_SESSION, item_id, student_mail, permission))
        
        

