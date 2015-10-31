import json
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import httplib2
from drive_api import Drive

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'
CACHE_MAX_AGE = 60*5 # cache set to 5 minutes

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
    # Drive.refresh()
    try:
      show_items(user_input)
    except:
      show_login()
      wf.send_feedback()

  return 0

def show_items(user_input):
  links = wf.cached_data('api_results', Drive.get_links, CACHE_MAX_AGE)
  try:
    links = wf.filter(query=user_input,items=links,key=lambda x : x['title'])
  except:
    links = []

  if len(links):
    add_items(links)
  else:
    wf.add_item(
      title='No files found',
      icon=ICON_WARNING,
    )
  wf.send_feedback()

def add_items(links):
  wf.logger.error('there are links')
  # sorted(links, key=lambda link : link['lastViewedByMeDate'])
  for index, link in enumerate(links):
    title = link['title']
    alternateLink = link['alternateLink']
    icon = link['icon']
    wf.add_item(
      title=title,
      arg=alternateLink,
      icon=icon,
      valid=True
    )

def show_login():
  wf.add_item(title='d > login',
    arg='login' + Drive.get_auth_url(),
    icon=ICON_USER,
    autocomplete='> login',
    valid=True)

def show_options(user_input):
  if user_input in 'login':
    show_login()
  ## add another condition
  if user_input in 'logout':
    wf.add_item(title='d > logout',
      arg='logout',
      autocomplete='> logout',
      icon=ICON_USER,
      valid=True)

if __name__ == '__main__':
  wf.run(main)