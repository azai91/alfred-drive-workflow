import json
import subprocess
from config import CLIENT_ID, CLIENT_SECRET, SCOPE, REDIRECT_URI, FILES_URL, AUTH_URL, TOKEN_URL, TOKEN_URL, CACHE_MAX_AGE, LOGIN, LOGOUT, SET_CACHE, CLEAR_CACHE, INVALID, CONNECTION_ERROR
import requests
import util
from workflow import Workflow, ICON_EJECT, ICON_ACCOUNT, ICON_BURN, ICON_CLOCK, ICON_WARNING
from workflow.background import is_running, run_in_background
UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

class Drive:

    @classmethod
    def open_auth_page(cls):
        cls.start_auth_server()
        subprocess.call(['open', AUTH_URL])

    @classmethod
    def start_auth_server(cls):
        subprocess.Popen(['nohup','python','./server.py'])

    @classmethod
    def exchange_tokens(cls, code):
        response = requests.post(TOKEN_URL,{
            'code': code,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET,
            'redirect_uri' : REDIRECT_URI,
            'grant_type' : 'authorization_code'
        }).json()
        wf.save_password('access_token', response['access_token'])
        wf.save_password('refresh_token', response['refresh_token'])

    @classmethod
    def get_request_token(cls):
        cls.start_server()
        subprocess.call(['open', cls.get_auth_url()])

    @classmethod
    def delete_credentials(cls):
        wf.delete_password('access_token','')

    @classmethod
    def get_access_token(cls):
        return wf.get_password('access_token')

    @classmethod
    def refresh(cls):
        refresh_token = wf.get_password('refresh_token')
        try:
            response = requests.post(TOKEN_URL,{
                'client_id' : CLIENT_ID,
                'client_secret' : CLIENT_SECRET,
                'refresh_token' : refresh_token,
                'grant_type' : 'refresh_token'
            }).json()
            wf.save_password('access_token', response['access_token'])
            return 1
        except:
            wf.logger.error('Error Refreshing')
            return 0

    @classmethod
    def get_links(cls, tries=10):
        links = wf.cached_data('drive_api_results', max_age=120)
        # Wait for data
        while links is None:
            cls.refresh_list()
            sleep(0.5)
            links = wf.cached_data('drive_api_results', max_age=120)
            if tries > 0:
                tries -= 1
            else:
                return []
        return links

    @classmethod
    def refresh_list(cls):
        if not is_running('drive_refresh'):
            cmd = ['/usr/bin/python', wf.workflowfile('drive_refresh.py')]
            run_in_background('drive_refresh', cmd)

    @classmethod
    def open_page(cls,url):
        subprocess.call(['open',url])

    @classmethod
    def revoke_token(cls):
        access_token = wf.save_password('access_token','')
        return requests.get('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)

    @classmethod
    def show_items(cls, user_input):
        cache_length = CACHE_MAX_AGE
        if not wf.get_password('access_token'):
            raise Exception('No access token found')
        if wf.stored_data('cache_length'):
            cache_length = wf.stored_data('cache_length')

        # # if util.internet_on():
        #     links = wf.cached_data('drive_api_results', cls.get_links, cache_length)
        # else:
        #     cls.show_error('ConnectionError')
        #     d return wf.send_feedback()

        links = wf.cached_data('drive_api_results')

        # internet
        # try:

        # except requests.ConnectionError:


        try:
            links = wf.filter(query=user_input, items=links, key=lambda x : x['title'])
        except:
            links = []

        if len(links):
            add_items(links)
        else:
            # place in config
            wf.add_item(
                title='No files found',
                icon=ICON_WARNING)

        wf.send_feedback()

    @classmethod
    def show_options(cls, user_input):
        if 'login'.startswith(user_input.lower()):
            cls.show_login()
        ## add another condition
        if 'logout'.startswith(user_input.lower()):
            cls.show_logout()
        if 'clear cache'.startswith(user_input.lower()):
            cls.show_clear_cache()
        if 'set cache length'.startswith(user_input[:16].lower()):
            cls.show_set_cache_length(user_input[17:])

        if len(wf._items) == 0:
            cls.show_invalid_option()

        wf.send_feedback()

    @classmethod
    def show_login(cls):
        wf.add_item(title=LOGIN['title'],
            arg=LOGIN['arg'],
            icon=LOGIN['icon'],
            autocomplete=LOGIN['autocomplete'],
            valid=True)

    @classmethod
    def show_logout(cls):
        wf.add_item(title=LOGOUT['title'],
            arg=LOGOUT['arg'],
            autocomplete=LOGOUT['autocomplete'],
            icon=LOGOUT['icon'],
            valid=True)

    @classmethod
    def show_clear_cache(cls):
        wf.add_item(title=CLEAR_CACHE['title'],
            arg=CLEAR_CACHE['arg'],
            autocomplete=CLEAR_CACHE['autocomplete'],
            icon=CLEAR_CACHE['icon'],
            valid=True)

    @classmethod
    def show_set_cache_length(cls, length):
        if not len(length):
            wf.add_item(title=SET_CACHE['title'] % '[seconds]',
                autocomplete=SET_CACHE['autocomplete'],
                icon=SET_CACHE['icon'])
        else:
            try:
                int(length)
                wf.add_item(title=SET_CACHE['title'] % util.convert_time(length),
                    arg=SET_CACHE['arg'] % length,
                    icon=SET_CACHE['icon'],
                    valid=True)
            except:
                wf.add_item(title='please insert valid cache length',
                    icon=ICON_CLOCK)

    @classmethod
    def show_invalid_option(cls):
            """Display invalid option"""

            wf.add_item(title=INVALID['title'],
                                    icon=INVALID['icon'])

    @classmethod
    def show_error(cls, error):
        if error == 'ConnectionError':
            ERROR = CONNECTION_ERROR

        wf.add_item(title=ERROR['title'], icon=ERROR['icon'])

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
        wf.store_data('cache_length', length)

def add_items(links):
    # sorted(links, key=lambda link : link['lastViewedByMeDate'])
    for index, link in enumerate(links):
        title = link['title']
        alternateLink = link['alternateLink']
        icon = link['icon']
        wf.add_item(
            title=title,
            arg=alternateLink,
            icon=icon,
            valid=True)

