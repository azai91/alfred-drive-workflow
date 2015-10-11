from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
wf = Workflow()
from drive_api import Drive
import httplib2
import json

class Search:
  def __init__(self,user_input):
    self.user_input = user_input

  #TODO: use wf.stored_data
  def get_links(self):
    wf.logger.error('im inside')
    wf.logger.error(self.user_input)
    user_input = escape_term(self.user_input)
    wf.logger.error('im inside')
    user_credentials = Drive.get_credentials()
    http = httplib2.Http()
    http = user_credentials.authorize(http)
    wf.logger.error('im inside')
    url = 'https://www.googleapis.com/drive/v2/files?q=title+contains+\'%s\'&key=AIzaSyAMhz8CJf7_xLUquUNdpvTF42fIDk7NALs' % user_input
    wf.logger.error(url)
    (resp_headers, content) = http.request(url,'GET')
    return json.loads(content)['items']

  def show_items(self):
    wf.logger.error('hello')
    wf.logger.error('before')
    links = wf.cached_data(self.user_input, self.get_links)
    # place somewhere else
    wf.logger.error('hi')
    self.add_items(links)

  def add_items(self, links):
    wf.logger.error('there')
    if len(links):
      wf.logger.error('there are links')
      # sorted(links, key=lambda link : link['lastViewedByMeDate'])
      count = 0
      for index, link in enumerate(links):
        type = ''
        try:
          type = link['mimeType'].split('.')[2]
        except:
          wf.logger.error('title' + link['mimeType'])
        if type == 'spreadsheet' or type == 'document':
          icon = './assets/sheets.png' if type == 'spreadsheet' else './assets/docs.png'
          count += 1
          title = link['title']
          alternateLink = link['alternateLink']
          wf.add_item(
            title=title,
            arg=alternateLink,
            icon=icon,
            valid=True
          )
      wf.logger.error('ending')
      if count == 0:
        wf.add_item(
          title='No files found',
          icon=ICON_WARNING,
        )
    else:
      wf.add_item(
        title='No files found',
        icon=ICON_WARNING,
      )
    wf.logger.error('ending there')
    wf.send_feedback()

def escape_term(term):
  return term.replace(' ', '+')

