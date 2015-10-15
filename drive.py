import json
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import sys
import subprocess
import oauth
import httplib2
from drive_api import Drive
from search import Search

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
    wf.send_feedback()
  elif len(user_input):
    search = Search(user_input)
    Drive.refresh()
    try:
      search.show_items()
      wf.logger.error('there are things')
    except:
      wf.add_item(title='Drive > login',
        arg=Drive.get_auth_url(),
        icon=ICON_USER,
        valid=True)
      wf.send_feedback()

  return 0

def show_options(user_input):
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

if __name__ == '__main__':
  wf.run(main)