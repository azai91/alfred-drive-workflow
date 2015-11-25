"""
Update items list
"""

from workflow import Workflow, ICON_EJECT, ICON_ACCOUNT, ICON_BURN, ICON_CLOCK, PasswordNotFound
UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'
from drive_api import Drive
import util
from config import FILES_URL
import requests
import sys
import urllib2

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main():
    try:
        # test if internet is working
        urllib2.urlopen('http://google.com',timeout=1)
        results = Drive.get_links()
        wf.cache_data('drive_api_results', results)
        wf.cache_data('drive_error', None) #No error if able to make requests
    except (requests.ConnectionError, PasswordNotFound, urllib2.URLError), e:
        error = type(e).__name__
        print error
        if error == 'URLError':
            error = 'ConnectionError'
        print error
        wf.cache_data('drive_error', error)

if __name__ == '__main__':
    main() # pragma: no cover
