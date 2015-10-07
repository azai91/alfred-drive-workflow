import json
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import sys
import subprocess
import oauth
import httplib2

log = None

def main(wf):
  user_input = wf.args[0]
  command = user_input.split()[0]
  options = user_input[len(command) + 1:]

  if command == '>':
    if options in 'login' and not wf.stored_data('google_drive_oauth_code'):
      wf.add_item(title='Drive > login',
          arg=prepend_action_string('login',oauth.get_auth_url()),
          icon=ICON_USER,
          subtitle='Login',
          valid=True)
    if options in 'logout' and wf.stored_data('google_drive_oauth_code'):
      wf.add_item(title='Drive > logout',
        arg='logout',
        icon=ICON_USER,
        valid=True)
    wf.send_feedback()
    return 0
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
      arg=prepend_action_string('login', oauth.get_auth_url()),
      icon=ICON_USER,
      subtitle=get_auth_url(),
      valid=True)

  wf.send_feedback()
  return 0

def prepend_action_string(action, string):
  return action + string

if __name__ == '__main__':
  wf = Workflow()
  log = wf.logger
  sys.exit(wf.run(main))
