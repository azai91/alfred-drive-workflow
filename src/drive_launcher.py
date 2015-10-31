import subprocess
import sys
from drive_api import Drive
from workflow import Workflow

def main(wf):
  url = wf.args[0]
  if url in 'logout':
    Drive.delete_credentials()
    return None
  elif url[:5] in 'login':
    Drive.open_auth_page()
    return None

  subprocess.call(['open',url])

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
