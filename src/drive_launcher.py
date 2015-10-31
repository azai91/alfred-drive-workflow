import sys
from drive_api import Drive

def main(wf):
  url = wf.args[0]
  if url in 'logout':
    return Drive.delete_credentials()
  elif url[:5] in 'login':
    return Drive.open_auth_page()
  Drive.open_page(url)

if __name__ == '__main__':
  sys.exit(wf.run(main))
