import workflow.web as request
import json
from functools import wraps
import subprocess
import os
import signal
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
flow = OAuth2WebServerFlow(client_id='978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com', client_secret='rty2NIATZfWFWSDX-XPs2usX', scope='https://www.googleapis.com/auth/drive', redirect_uri='http://localhost:1337')

flow.params['access_type'] = 'offline'
storage = Storage('./credentials')
wf = Workflow()


class DriveExeption(Exception):
  pass

class AuthException(Exception):
  pass

class Drive():

  @classmethod
  def verify_credentials(cls, code):
    return flow.step2_exchange(code)

  @classmethod
  def store_request_token(cls, code):
    wf.cache_data('drive_request_token', code)

  @classmethod
  def get_auth_url(cls):
    return 'login' + flow.step1_get_authorize_url()

  @classmethod
  def start_server(cls):
    subprocess.Popen(['nohup','python','./server.py'])

  @classmethod
  def get_request_token(cls):
    cls.start_server()
    subprocess.call(['open', cls.get_auth_url()])
    # wf.cache_data('request_token', request_token)
    # auth_url = Drive.get_auth_url()

  @classmethod
  def save_credentials(cls, credentials):
    storage.put(credentials)

  @classmethod
  def get_credentials(cls):
    return storage.get()

