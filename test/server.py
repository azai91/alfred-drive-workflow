from flask import Flask, request
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import os
from oauth2client.client import OAuth2WebServerFlow
from action import stopServer
app = Flask(__name__)

flow = OAuth2WebServerFlow(client_id='978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com',
    client_secret='rty2NIATZfWFWSDX-XPs2usX',
    scope='https://www.googleapis.com/auth/drive',
    redirect_uri='http://localhost:1337')


@app.route('/')
def default():
    code = request.args.get('code')
    credentials = flow.step2_exchange(code)
    wf = Workflow()
    wf.store_data('google_drive_oauth_code', credentials)
    return 'Thank you for your code'

def write_pid():
    target = open('./pid.py', 'a')
    target.write(str(os.getpid()))
    target.write('\n')
    target.close()

if __name__ == '__main__':
    stopServer()
    write_pid()
    app.run(host='localhost', port=1337)
