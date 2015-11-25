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
        results = make_request()
        wf.cache_data('drive_api_results', results)
    # # except :
    #     e = sys.exc_info()[0]
    #     print e
    #     error = type(e).__name__
    #     print error
    #     wf.cache_data('drive_error', error)


def make_request():
    access_token = Drive.get_access_token()
    headers = {
        'Authorization' : 'Bearer %s' % access_token
    }
    response = requests.get(FILES_URL, headers=headers).json()
    unfiltered_list = response['items']
    return util.filter_by_file_type(unfiltered_list,['spreadsheet','document'])

if __name__ == '__main__':
    main() # pragma: no cover
