from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
wf = Workflow()
from drive_api import Drive
import httplib2
import json
max_age = 86400 # cache set to one day

class Search:
  def __init__(self,user_input):
    self.user_input = user_input

  def show_items(self):
    links = wf.cached_data(self.user_input,self.get_links,max_age=max_age)
    self.add_items(links)

  #TODO: use wf.stored_data
  def get_links(self):
    user_input = escape_term(self.user_input)
    user_credentials = Drive.get_credentials()
    http = httplib2.Http()
    http = user_credentials.authorize(http)
    url = 'https://www.googleapis.com/drive/v2/files?q=title+contains+\'%s\'&key=AIzaSyAMhz8CJf7_xLUquUNdpvTF42fIDk7NALs' % user_input
    (resp_headers, content) = http.request(url,'GET')
    return json.loads(content)['items']

  def add_items(self, links):
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
    wf.send_feedback()

def escape_term(term):
  return term.replace(' ', '+')

