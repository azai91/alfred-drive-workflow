"""Basic utility library"""

import urllib2

def convert_time(seconds):
    if seconds == '1':
        return '%s second' % seconds
    return '%s seconds' % seconds

def internet_on():
    try:
        response = urllib2.urlopen('http://google.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def filter_by_file_type(list, file_types):
    filter_list = []
    for index, link in enumerate(list):
        type = ''
        try:
            type = link['mimeType'].split('.')[2]
        except:
            pass
        if type in file_types:
            # refactor
            icon = './icons/sheets.png' if type == 'spreadsheet' else './icons/docs.png'
            link['icon'] = icon
            link['type'] = type
            filter_list.append(link)
    return filter_list
