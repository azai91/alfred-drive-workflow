import sys
from drive_api import Drive
from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(wf):
  url = wf.args[0]
  if url in 'logout':
    return Drive.delete_credentials()
  elif url[:5] in 'login':
    return Drive.open_auth_page()
  Drive.open_page(url)

if __name__ == '__main__':
  sys.exit(wf.run(main))
