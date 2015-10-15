import json
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import httplib2
from drive_api import Drive
from search import Search

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):
  user_input = ""
  options = True if wf.args[0][0] == '>' else False

  if wf.update_available:
    wf.add_item(
      'An update is available!',
      autocomplete='workflow:update',
      valid=False
    )

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
      arg='login' + Drive.get_auth_url(),
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