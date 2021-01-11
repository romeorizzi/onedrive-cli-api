from auth import device_flow_session, api_endpoint
import os
import sys

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
else:
    print('Available options: -r or -w')
    sys.exit()

GRAPH_SESSION = device_flow_session()
if GRAPH_SESSION:
    item_id = get_item_id(GRAPH_SESSION, item_path)
    print(invite_student(GRAPH_SESSION,item_id,student_mail,permission))