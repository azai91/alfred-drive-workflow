import json
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
from oauth2client.client import OAuth2WebServerFlow
import httplib2
import sys
import subprocess

flow = OAuth2WebServerFlow(client_id='978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com',
    client_secret='rty2NIATZfWFWSDX-XPs2usX',
    scope='https://www.googleapis.com/auth/drive',
    redirect_uri='http://localhost:3000')

log = None

def main(wf):
    user_input = wf.args[0]
    command = user_input.split()[0]
    options = user_input[len(command) + 1:]

    if command == '>':
        if options in 'login':
            wf.add_item(title='Drive > login',
                arg=prepend_action_string('login', get_auth_url()),
                icon=ICON_USER,
                subtitle=get_auth_url(),
                valid=True)
        if options in 'logout':
            wf.add_item(title='Drive > logout',
                arg='logout',
                icon=ICON_USER,
                subtitle=get_auth_url(),
                valid=True)
    elif wf.stored_data('google_drive_oauth_code'):
        credentials = wf.stored_data('google_drive_oauth_code')
        http = httplib2.Http()
        http = credentials.authorize(http)
        (resp_headers, content) = http.request('https://www.googleapis.com/drive/v2/files?q=title+contains+%22' +command +'%22&key=AIzaSyAMhz8CJf7_xLUquUNdpvTF42fIDk7NALs','GET')
        results = json.loads(content)['items']
        for result in results:
            type = ""
            try:
                type = result['mimeType'].split('.')[2]
            except:
                type = ""
            if type == 'spreadsheet':
                wf.add_item(title=result['title'],
                    arg=result['alternateLink'],
                    icon='./assets/sheets.png',
                    valid=True)
            elif type == 'document':
                wf.add_item(title=result['title'],
                    arg=result['alternateLink'],
                    icon='./assets/docs.png',
                    valid=True)
        if len(results) == 0:
            wf.add_item(title="No Results Found",
                icon=ICON_WARNING)
            wf.send_feedback()
            return 0
    else:
        wf.add_item(title='Drive > login',
            arg=prepend_action_string('login', get_auth_url()),
            icon=ICON_USER,
            subtitle=get_auth_url(),
            valid=True)

    wf.send_feedback()
    return 0

def get_auth_url():
    return flow.step1_get_authorize_url()

def add_credentials(code):
    try:
        credentials = flow.step2_exchange(code)
        wf.store_data('google_drive_oauth_code', credentials)
        return True
    except:
        return False

def prepend_action_string(action, string):
    return action +string


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
