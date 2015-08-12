import webbrowser
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import sys
import signal
import subprocess
import os

log = None

def main(wf):
    url = wf.args[0]
    stopServer()
    if url in 'logout':
        wf.store_data('google_drive_oauth_code','')
        return 0
    elif url[:5] in 'login':
        startServer()
        url = str(url[5:])
    webbrowser.open_new_tab(url)

def startServer():
    subprocess.Popen(['nohup','python','./server.py'])

def stopServer():
    target = open('./pid.py','r+')
    pids = target.read().split('\n')
    for pid in pids:
        try:
            os.kill(int(pid), signal.SIGKILL)
        except:
            a = 'hi'
    target.truncate()
    target.close()
    open('./pid.py','w').close()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
