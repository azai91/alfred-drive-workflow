import workflow.web as requests
import json
import httplib2
from oauth2client.client import OAuth2WebServerFlow
from keys import client_id, client_secret, scope, redirect_uri

from workflow import Workflow
flow = OAuth2WebServerFlow(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)
flow.params['access_type'] = 'offline'
auth_url = 'https://accounts.google.com/o/oauth2/auth?scope=%s&redirect_uri=%s&response_type=code&client_id=%s&access_type=offline&approval_prompt=force' % (scope,redirect_uri,client_id)

files_url='https://www.googleapis.com/drive/v2/files?orderBy=lastViewedByMeDate+desc'

wf = Workflow()

class DriveExeption(Exception):
  pass

class AuthException(Exception):
  pass

class Drive:

  @classmethod
  def get_auth_url(cls):
    return auth_url

  @classmethod
  def verify_credentials(cls, consumer_key):
    # headers = {
    #   'Content-Type': 'application/x-www-form-urlencoded',
    # }
    # url = 'https://www.googleapis.com/oauth2/v3/token'
    # params = {
    #   'code': consumer_key,
    #   'client_id' : client_id,
    #   'client_secret' : client_secret,
    #   'redirect_uri' : redirect_uri,
    #   'grant_type' : 'authorization_code'
    # }
    # return requests.post(url,params=params)
    return flow.step2_exchange(consumer_key)

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
    # storage.delete()

  @classmethod
  def refresh(cls):
    try:
      user_credentials = cls.get_credentials()
      user_credentials.refresh(httplib2.Http())
      user_credentials = cls.save_credentials(user_credentials)
    except:
      wf.logger.error('Error Refreshing')

  @classmethod
  def get_links(cls):
    wf.logger.error('CALLED')
    user_credentials = cls.get_credentials()
    http = httplib2.Http()
    wf.logger.error('getting crednetails')
    http = user_credentials.authorize(http)
    (resp_headers, content) = http.request(files_url,'GET')
    wf.logger.error('getting crednetails')
    unfiltered_list = json.loads(content)['items']
    return filter_by_file_type(unfiltered_list,['spreadsheet','document'])

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

