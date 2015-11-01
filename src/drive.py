from workflow import Workflow
from drive_api import Drive

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):
  user_input = ""
  options = True if wf.args[0][0] == '>' else False

  if wf.update_available:
    Drive.add_update()

  try:
    user_input = wf.args[0][1::].strip() if options else wf.args[0]
  except:
    user_input = wf.args[0]

  if options:
    Drive.show_options(user_input)
  elif len(user_input):
    try:
      Drive.show_items(user_input)
    except:
      Drive.show_login()

  return 0

if __name__ == '__main__':
  wf.run(main)