# A simple script will that will serve files thru HTTPS,
# based on the directory which it's run from.

import BaseHTTPServer, SimpleHTTPServer
import ssl
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'localhost.pem')

httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', 443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile=filename, server_side=True)
httpd.serve_forever()
