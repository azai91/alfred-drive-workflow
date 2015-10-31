import workflow.web as requests
import json
import httplib2
import subprocess
from oauth2client.client import OAuth2WebServerFlow
from config import CLIENT_ID, CLIENT_SECRET, SCOPE, REDIRECT_URI
import requests

from workflow import Workflow
flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
flow.params['access_type'] = 'offline'
auth_url = 'https://accounts.google.com/o/oauth2/auth?scope=%s&redirect_uri=%s&response_type=code&client_id=%s&access_type=offline&approval_prompt=force' % (SCOPE,REDIRECT_URI,CLIENT_ID)

token_url = 'https://www.googleapis.com/oauth2/v3/token'
files_url='https://www.googleapis.com/drive/v2/files?orderBy=lastViewedByMeDate+desc&fields=items'

wf = Workflow()

class DriveExeption(Exception):
  pass

class AuthException(Exception):
  pass

class Drive:

  @classmethod
  def open_auth_page(cls):
    cls.start_auth_server()
    subprocess.call(['open', auth_url])

  @classmethod
  def start_auth_server(cls):
    subprocess.Popen(['nohup','python','./server.py'])

  @classmethod
  def exchange_tokens(cls, code):
    # headers = {
    #   'Content-Type': 'application/x-www-form-urlencoded',
    # }
    response = requests.post(token_url,{
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
  def save_credentials(cls, credentials):
    wf.store_data('credentials', credentials)

  @classmethod
  def get_credentials(cls):
    return wf.stored_data('credentials')

  @classmethod
  def delete_credentials(cls):
    wf.store_data('credentials','')

  @classmethod
  def refresh(cls):
    refresh_token = wf.get_password('refresh_token')
    try:
      response = requests.post(token_url,{
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'refresh_token' : refresh_token,
        'grant_type' : 'refresh_token'
      }).json()
      wf.save_password('access_token', response['access_token'])
    except:
      wf.logger.error('Error Refreshing')

  @classmethod
  def get_links(cls):
    access_token = wf.get_password('access_token')
    headers = {
      'Authorization' : 'Bearer %s' % access_token
    }
    response = requests.get(files_url,headers=headers).json()
    return response
    # unfiltered_list = response['items']
    # return filter_by_file_type(unfiltered_list,['spreadsheet','document'])

  @classmethod
  def revoke_token(cls):
    access_token = wf.get_password('access_token')
    return requests.get('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)

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

