import json
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import sys
import subprocess
import oauth
import httplib2
from drive_api import Drive

log = None
wf = Workflow()

def main(_):
  user_input = ""
  options = True if wf.args[0][0] == '>' else False

  try:
    user_input = wf.args[0][1::].strip() if options else wf.args[0]
  except:
    user_input = wf.args[0]

  if options:
    show_options(user_input)
  else:
    show_items(user_input)

  wf.send_feedback()
  return 0

def show_items(user_input):
  Drive.refresh()

  if len(user_input):
    try:
      links = get_links(user_input)
      add_items(links, user_input)
    except:
      wf.add_item(title='Drive > login',
        arg=Drive.get_auth_url(),
        icon=ICON_USER,
        valid=True)

def show_options(user_input):
  wf.logger.error('optoins')
  if user_input in 'login':
    wf.add_item(title='Drive > login',
      arg='login' + oauth.get_auth_url(),
      icon=ICON_USER,
      valid=True)
  ## add another condition
  if user_input in 'logout':
    wf.add_item(title='Drive > logout',
      arg='logout',
      icon=ICON_USER,
      valid=True)

def add_items(links, user_input):
  if len(links):
    wf.logger.error('there are links')
    # sorted(links, key=lambda link : link['lastViewedByMeDate'])
    count = 0
    for index, link in enumerate(links):
      type = ''
      try:
        type = link['mimeType'].split('.')[2]
      except:
        wf.logger.error('title' + link['mimeType'])
      if type == 'spreadsheet' or type == 'document':
        icon = './assets/sheets.png' if type == 'spreadsheet' else './assets/docs.png'
        count += 1
        title = link['title']
        alternateLink = link['alternateLink']
        wf.add_item(
          title=title,
          arg=alternateLink,
          icon=icon,
          valid=True
        )
    if count == 0:
      wf.add_item(
        title='No files found',
        icon=ICON_WARNING,
      )
  else:
    wf.add_item(
      title='No files found',
      icon=ICON_WARNING,
    )

#TODO: use wf.stored_data
def get_links(term):
  term = escape_term(term)
  user_credentials = Drive.get_credentials()
  wf.logger.error('1')
  http = httplib2.Http()
  http = user_credentials.authorize(http)
  wf.logger.error(term)
  url = 'https://www.googleapis.com/drive/v2/files?q=title+contains+\'%s\'&key=AIzaSyAMhz8CJf7_xLUquUNdpvTF42fIDk7NALs' % term
  wf.logger.error(url)
  (resp_headers, content) = http.request(url,'GET')
  wf.logger.error('get workded')
  return json.loads(content)['items']

def escape_term(term):
  return term.replace(' ', '+')

if __name__ == '__main__':
  wf.run(main)