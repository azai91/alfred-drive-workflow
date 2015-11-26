import sys
from drive_api import Drive
from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(wf):
    url = wf.args[0]
    if url == 'logout':
        Drive.revoke_tokens()
        return sys.stdout.write('logged out')
    elif url == 'login':
        return Drive.open_auth_page()
    elif url == 'clear':
        Drive.clear_cache()
        return sys.stdout.write('cache cleared')
    elif url.startswith('set'):
        length = int(url[3:])
        Drive.set_cache_length(length)
        return sys.stdout.write('cache set to %s seconds' % str(length))

    Drive.open_page(url)

if __name__ == '__main__':
    sys.exit(wf.run(main))
