import os
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from oauth2client.client import OAuth2WebServerFlow
from action import stopServer
import urlparse
import oauth


def write_pid():
  target = open('./pid.py', 'a')
  target.write(str(os.getpid()))
  target.write('\n')
  target.close()

class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(s):
    try:
      code = urlparse.urlparse(s.path)[4].split('=')[1]
      oauth.add_credentials(code)
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
