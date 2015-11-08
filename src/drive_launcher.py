import sys
from drive_api import Drive
from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(wf):
  url = wf.args[0]
  if url[:6] in 'logout':
    return Drive.delete_credentials()
  elif url[:5] in 'login':
    return Drive.open_auth_page()
  elif url[:5] in 'clear':
    Drive.clear_cache()
    return sys.stdout.write("cache cleared")
  elif url[:3] in 'set':
    length = int(url[3:])
    Drive.set_cache_length(length)
    return sys.stdout.write("cache set to " + str(length))

  Drive.open_page(url)

if __name__ == '__main__':
  sys.exit(wf.run(main))
