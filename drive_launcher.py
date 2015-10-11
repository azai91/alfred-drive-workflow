import webbrowser
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import sys
import signal
import subprocess
import os
from drive import Drive

log = None

def main(wf):
    url = wf.args[0]
    # stopServer()
    if url in 'logout':
        Drive.delete_credentials()
        return None
    elif url[:5] in 'login':
        start_server()
        url = str(url[5:])
    subprocess.call(['open',url])

def start_server():
    subprocess.Popen(['nohup','python','./server.py'])

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
