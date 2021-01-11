from auth import device_flow_session, api_endpoint
import os
import sys

def get_item_id(session, item_path):
    fname_only = os.path.basename(item_path)
    print(f'Getting id of {fname_only}')
    endpoint = f'/me/drive/root:/{item_path}'
    response = session.get(api_endpoint(endpoint))
    return response.json()['id']


def get_all_file(session, folder_id):
    endpoint = f'/me/drive/items/{folder_id}/children'
    response = session.get(api_endpoint(endpoint))
    all_items = []
    for d in response.json()['value']:
        print(f'Getting permission of {d["name"]}')
        all_items.append(d['id'])
    return (all_items)


def get_permissions(session, item_id):
    endpoint = f'/me/drive/items/{item_id}/permissions'
    response = session.get(api_endpoint(endpoint))
    return response.json()['value'][0]['id']


def remove_permissions(session, item_id, perm_id):
    endpoint = f'/me/drive/items/{item_id}/permissions/{perm_id}'
    response = session.delete(api_endpoint(endpoint))
    return (response)


if len(sys.argv) != 3:
    print("Usage: ./rm_permissions.py folder/item_path -f|-i")
    print("Example: ./rm_permissions.py esamiRO/2020-07-27/id076596 -f --> remove folder and children's folder permissions\n"
          "Example: ./rm_permissions.py esamiRO/2020-07-27/id076596 -i --> remove item permission only")
    sys.exit()

item_path = sys.argv[1]

GRAPH_SESSION = device_flow_session()
if GRAPH_SESSION:
    item_id = get_item_id(GRAPH_SESSION, item_path)
    permission_id = get_permissions(GRAPH_SESSION, item_id)
    print(remove_permissions(GRAPH_SESSION, item_id, permission_id))
    if sys.argv[2] == '-f':
        items_id_in_folder = get_all_file(GRAPH_SESSION, item_id)
        for id in items_id_in_folder:
            permission_id = get_permissions(GRAPH_SESSION, id)
            print(remove_permissions(GRAPH_SESSION, id, permission_id))