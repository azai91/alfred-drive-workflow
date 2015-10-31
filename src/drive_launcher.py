import subprocess
import sys
from drive_api import Drive
from workflow import Workflow

def main(wf):
  url = wf.args[0]
  if url in 'logout':
    return Drive.delete_credentials()
  elif url[:5] in 'login':
    return Drive.open_auth_page()
  Drive.open_page(url)

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
