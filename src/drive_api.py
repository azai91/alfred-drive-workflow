import json
import subprocess
from config import *
import requests
import util
from time import sleep
from workflow import *
from workflow.background import is_running, run_in_background
UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

class Drive:

    @classmethod
    def open_auth_page(cls):
        """Starts server for redirect uri and opens
        authenicatin page
        """

        subprocess.Popen(['nohup', 'python', './server.py'])
        subprocess.call(['open', AUTH_URL])

    @classmethod
    def exchange_tokens(cls, code):
        """Exchange code for access and refresh token

        Store tokens in workflow
        """

        response = requests.post(TOKEN_URL, {
            'code': code,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET,
            'redirect_uri' : REDIRECT_URI,
            'grant_type' : 'authorization_code'
        }).json()
        wf.save_password('drive_access_token', response['access_token'])
        wf.save_password('drive_refresh_token', response['refresh_token'])

    @classmethod
    def revoke_tokens(cls):
        """Revoke and delete tokens"""

        access_token = wf.get_password('drive_access_token')
        requests.get('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)
        wf.delete_password('drive_access_token')
        wf.delete_password('drive_refresh_token')

    @classmethod
    def refresh(cls):
        """Refresh access token"""

        refresh_token = wf.get_password('drive_refresh_token')
        try:
            response = requests.post(TOKEN_URL, {
                'client_id' : CLIENT_ID,
                'client_secret' : CLIENT_SECRET,
                'refresh_token' : refresh_token,
                'grant_type' : 'refresh_token'
            }).json()
            wf.save_password('drive_access_token', response['access_token'])
            return 1
        except:
            wf.logger.error('Error Refreshing')
            return 0

    @classmethod
    def get_links(cls):
        """Get all files from google drive_refresh

        Returns:
            a list of all spreadsheets and documents from Google Drive
        """
        access_token = wf.get_password('drive_access_token')
        headers = {
            'Authorization' : 'Bearer %s' % access_token
        }
        response = requests.get(FILES_URL, headers=headers).json()
        # TODO: Log errors to alfred bar
        if 'error' in response and cls.refresh():
            return cls.get_links()

        items = response['items']
        while 'nextPageToken' in response:
            nextPageToken = response['nextPageToken']
            response = requests.get(FILES_URL + '&pageToken=' + nextPageToken, headers=headers).json()
            items += response['items']

        return items

    @classmethod
    def refresh_list(cls):
        """Spawn subprocess to populate response from Google Drive"""

        if not is_running('drive_refresh'):
            cmd = ['/usr/bin/python', wf.workflowfile('drive_refresh.py')]
            run_in_background('drive_refresh', cmd)

    @classmethod
    def show_items(cls, user_input):
        cache_length = CACHE_MAX_AGE
        if wf.stored_data('drive_cache_length'):
            cache_length = wf.stored_data('cache_length')
        # check if any errors
        if wf.cached_data('drive_error', max_age=0):
            cls.show_error(wf.cached_data('drive_error', max_age=0))
            return wf.send_feedback()

        try:
            links = wf.cached_data('drive_api_results', cls.get_links, cache_length)
            all_parents = dict(zip(map((lambda item: item['id']), links), links))
            links = [item for item in links if item['mimeType'] != 'application/vnd.google-apps.folder']

            for item in links:
                path = []
                parents = item.get('parents', [])
                while len(parents):
                    if parents[0]['isRoot'] or not parents[0]['id'] in all_parents:
                        break
                    parent = all_parents[parents[0]['id']]
                    path.insert(0, parent['title'])
                    parents = parent.get('parents', [])
                item['x-path'] = '/'.join(path)

        except (requests.ConnectionError, PasswordNotFound), e:
            cls.show_error(type(e).__name__)
            return wf.send_feedback()

        try:
            links = wf.filter(query=user_input, items=links, key=lambda x : x['title'])
        except:
            links = []

        if len(links):
            cls.add_items(links)
        else:
            # place in config
            wf.add_item(
                title='No files found',
                icon=ICON_WARNING)

        wf.send_feedback()

    @classmethod
    def show_options(cls):
        """Show options"""

        for option in OPTIONS:
            wf.add_item(title=option['title'],
                autocomplete=option['autocomplete'])

        wf.send_feedback()

    @classmethod
    def show_settings(cls, user_input):
        """Show settings depending on user input

        Args:
            user_input, a string that contains users setting preference
        """

        actions = []
        for label in [ 'LOGIN', 'LOGOUT', 'CLEAR_CACHE' ]:
            actions.append(SETTINGS[label])

        actions.append({
            'title':        SETTINGS['SET_CACHE']['title'] % '[seconds]',
            'autocomplete': SETTINGS['SET_CACHE']['autocomplete'],
            'arg':          SETTINGS['SET_CACHE']['arg'],
            'icon':         SETTINGS['SET_CACHE']['icon'],
            'uid':          SETTINGS['SET_CACHE']['uid']
        })

         # if account is already set
        try:
            wf.get_password('drive_access_token')
            for label in [ 'DOC', 'SHEET', 'SLIDE', 'FORM' ]:
                actions.append(CREATE_SETTINGS[label])
        except: pass

        if len(user_input) > 0:
            actions = wf.filter(query=user_input, items=actions, key=lambda x : x['title'])

        if len(user_input) > 17 and user_input[:17].lower() == 'set cache length ':
            cls.show_set_cache_length(user_input[17:])
        else:
            for action in actions:
                wf.add_item(title=action['title'],
                    arg=action['arg'],
                    icon=action['icon'],
                    autocomplete=action['autocomplete'],
                    valid=True,
                    uid=action['uid'])

        if len(wf._items) == 0:
            cls.show_error('InvalidOption')

        wf.send_feedback()

    @classmethod
    def show_set_cache_length(cls, length):
        """Show set cache length setting"""

        try:
            int(length)
            wf.add_item(title=SETTINGS['SET_CACHE']['title'] % util.convert_time(length),
                arg=SETTINGS['SET_CACHE']['arg'] % length,
                icon=SETTINGS['SET_CACHE']['icon'],
                valid=True)
        except:
            wf.add_item(title='please insert valid cache length',
                icon=ICON_CLOCK)

    @classmethod
    def show_error(cls, error):
        """Displays error"""
        wf.add_item(title=ERRORS[error]['title'],
            icon=ERRORS[error]['icon'],
            valid=ERRORS[error]['valid'],
            arg=ERRORS[error]['arg'],
            subtitle=ERRORS[error]['subtitle'])

    @classmethod
    def add_update(cls):
        wf.add_item(
            'New version available!',
            'Action this item to install the update',
            autocomplete='workflow:update')

    @classmethod
    def clear_cache(cls):
        wf.clear_cache()

    @classmethod
    def set_cache_length(cls, length):
        wf.store_data('drive_cache_length', length)

    @classmethod
    def add_items(cls, links):
        for link in sorted(links, key=lambda link : link['title']):
            title = link['title']
            path = link.get('x-path', '')
            alternateLink = link['alternateLink']
            icon = util.find_icon(link)
            uid = link['id']
            wf.add_item(
                title=title,
                subtitle=path,
                arg=alternateLink,
                icon=icon,
                uid=uid,
                valid=True)

    @classmethod
    def create_file(cls, type):
        """
        Returns:
            a list of all spreadsheets and documents from Google Drive
        """

        access_token = wf.get_password('drive_access_token')
        headers = {
            'Authorization' : 'Bearer %s' % access_token,
            'Content-Type': 'application/json'
        }
        response = requests.post(CREATE_URL, headers=headers, data=json.dumps({
            'mimeType' : MIMETYPES[type]
            })).json()

        if 'error' in response and cls.refresh():
            return cls.create_file(type)
        
        return response['webViewLink']
        
        

