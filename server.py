from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import os
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from oauth2client.client import OAuth2WebServerFlow
from action import stopServer
import urlparse

flow = OAuth2WebServerFlow(client_id='978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com',
    client_secret='rty2NIATZfWFWSDX-XPs2usX',
    scope='https://www.googleapis.com/auth/drive',
    redirect_uri='http://localhost:1337')

def write_pid():
    target = open('./pid.py', 'a')
    target.write(str(os.getpid()))
    target.write('\n')
    target.close()

class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        try:
            code = urlparse.urlparse(s.path)[4].split('=')[1]
            credentials = flow.step2_exchange(code)
            wf = Workflow()
            wf.store_data('google_drive_oauth_code', credentials)
        except:
            pass
        s.wfile.write('Thank you for your code')

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

server_address = ('127.0.0.1', 1337)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
write_pid()

sa = httpd.socket.getsockname()
httpd.serve_forever()
