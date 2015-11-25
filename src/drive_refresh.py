"""
Update items list
"""

from workflow import Workflow, ICON_EJECT, ICON_ACCOUNT, ICON_BURN, ICON_CLOCK
UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'
from drive_api import Drive
import util
from config import FILES_URL
import requests
import sys

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main():
    try:
        results = Drive.get_links()
        wf.cache_data('drive_api_results', results)
        wf.cache_data('drive_error', None) #No error if able to make requests
    except requests.ConnectionError as b:
        e = sys.exc_info()[0]
        error = type(e).__name__
    #     print error
        wf.cache_data('drive_error', error)

if __name__ == '__main__':
    main() # pragma: no cover
