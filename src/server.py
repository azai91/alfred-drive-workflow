import os
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from oauth2client.client import OAuth2WebServerFlow
from drive_api import Drive
import urlparse

class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(s):
    try:
      code = urlparse.urlparse(s.path)[4].split('=')[1]
      user_credentials = Drive.verify_credentials(code)
      Drive.save_credentials(user_credentials)
      s.wfile.write('Your code has been saved in Alfred')
    except:
      s.wfile.write('Error' + code)

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

server_address = ('127.0.0.1', 1337)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
httpd.timeout = 20
httpd.handle_request()
