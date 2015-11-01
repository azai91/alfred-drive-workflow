import json
import subprocess
from config import CLIENT_ID, CLIENT_SECRET, SCOPE, REDIRECT_URI, FILES_URL, AUTH_URL, TOKEN_URL, TOKEN_URL, CACHE_MAX_AGE
import requests
from workflow import Workflow, ICON_USER
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
  def get_links(cls):
    access_token = wf.get_password('access_token')
    headers = {
      'Authorization' : 'Bearer %s' % access_token
    }
    response = requests.get(FILES_URL,headers=headers).json()
    if 'error' in response and cls.refresh():
      return cls.get_links()

    else:
      unfiltered_list = response['items']
      return filter_by_file_type(unfiltered_list,['spreadsheet','document'])

  @classmethod
  def open_page(cls,url):
    subprocess.call(['open',url])

  @classmethod
  def revoke_token(cls):
    access_token = wf.get_password('access_token')
    return requests.get('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)

  @classmethod
  def show_items(cls, user_input):
    links = wf.cached_data('api_results', cls.get_links,CACHE_MAX_AGE)
    try:
      links = wf.filter(query=user_input, items=links, key=lambda x : x['title'])
    except:
      links = []

    if len(links):
      add_items(links)
    else:
      wf.add_item(
        title='No files found',
        icon=ICON_WARNING)

    wf.send_feedback()

  @classmethod
  def show_options(cls,user_input):
    if user_input in 'login':
      cls.show_login()
    ## add another condition
    if user_input in 'logout':
      cls.show_logout()
    wf.send_feedback()

  @classmethod
  def show_login(cls):
    wf.add_item(title='d > login',
      arg='login',
      icon=ICON_USER,
      autocomplete='> login',
      valid=True)

  @classmethod
  def show_logout(cls):
    wf.add_item(title='d > logout',
      arg='logout',
      autocomplete='> logout',
      icon=ICON_USER,
      valid=True)

  @classmethod
  def add_update(cls):
    wf.add_item(
      'New version available!',
      'Action this item to install the update',
      autocomplete='workflow:update')

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

def filter_by_file_type(list, file_types):
  filter_list = []
  for index, link in enumerate(list):
    type = ''
    try:
      type = link['mimeType'].split('.')[2]
    except:
      wf.logger.error('title' + link['mimeType'])
    if type in file_types:
      # refactor
      icon = './icons/sheets.png' if type == 'spreadsheet' else './icons/docs.png'
      link['icon'] = icon
      link['type'] = type
      filter_list.append(link)
  return filter_list

