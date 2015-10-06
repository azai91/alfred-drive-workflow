from oauth2client.client import OAuth2WebServerFlow
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER

flow = OAuth2WebServerFlow(client_id='978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com', client_secret='rty2NIATZfWFWSDX-XPs2usX', scope='https://www.googleapis.com/auth/drive', redirect_uri='http://localhost:1337')

flow.params['access_type'] = 'offline'

def get_auth_url():
  return flow.step1_get_authorize_url()

def add_credentials(code):
  try:
    credentials = flow.step2_exchange(code)
    wf.store_data('google_drive_oauth_code', credentials)
    return True
  except:
    return False

wf = Workflow()

