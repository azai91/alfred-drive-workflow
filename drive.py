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
  # if wf.first_run:
    # wf.clear_cache()

  user_input = ""

  if len(wf.args):
    user_input = wf.args[0]

  try:
    wf.logger.error(not Drive.get_credentials().access_token_expired)
    if Drive.get_credentials().access_token_expired:
      refresh()
  except PasswordNotFound:
    wf.logger.error('not password')



  # links = get_links(user_input)

  try:
    links = get_links(user_input)
    wf.logger.error('c')
    wf.logger.error('made it')
    add_items(links, user_input)
    wf.logger.error('done')

  except:
    wf.add_item(title='Drive > login',
      arg=Drive.get_auth_url(),
      icon=ICON_USER,
      valid=True)

  wf.send_feedback()

  return 0

def authorize():
  request_token = wf.cached_data('drive_request_token')
  if request_token:
    wf.logger.error('drive reques token')
    try:
      user_credentials = Drive.verify_credentials(request_token)
      wf.logger.error('new crednetials')
      Drive.save_credentials(user_credentials)
      wf.logger.error('successfully')
      wf.clear_cache()
    except:
      wf.logger.error('RateLimitException')

def refresh():
  try:
    wf.logger.error('refreshgin')
    http = httplib2.Http()
    wf.logger.error('r1')
    user_credentials = Drive.get_credentials()
    wf.logger.error('r2')
    user_credentials.refresh(http)
    wf.logger.error('rdone')
    user_credentials = Drive.save_credentials()
  except:
    authorize()
    wf.logger.error('error refreshsing')

def prepend_action_string(action, string):
  return action + string

def add_items(links, user_input):
  # links = sorted()
  count = 0
  wf.logger.error('started')
  for index, link in enumerate(links):
    # wf.logger.error(link)
    # required_keys = ['title','mimeType','alternateLink']
    # if all(x in link for x in required_keys):
    type = ''
    # print 'there'
    try:
      type = link['mimeType'].split('.')[2]
    except:
      wf.logger.error('title' + link['mimeType'])
      pass
    # print type
    # wf.logger.error('title' + type)

    if type == 'spreadsheet' or type == 'document':
      icon = './assets/sheets.png' if type == 'spreadsheet' else './assets/docs.png'
      count += 1
      wf.logger.error('before')
      title = link['title']
      wf.logger.error('title' + title)
      alternateLink = link['alternateLink']
      wf.logger.error('alternateLink' + alternateLink)
      # print 'before'
      wf.add_item(
        title=title,
        arg=alternateLink,
        icon=icon,
        valid=True
      )
      # print 'after'
  if count == 0:
    wf.add_item(
      title='No files found',
      icon=ICON_WARNING,
    )

#use wf.stored data

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
  # print json.loads(content)
  return json.loads(content)['items']

def escape_term(term):
  return term.replace(' ', '+')

if __name__ == '__main__':
  wf.run(main)