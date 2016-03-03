import socket
import ssl
import re
import threading

import myserver
from mysettings import *

class https_server(myserver.WSGIServer):
    def __init__(self, application = None, SERVER_ADDR = (HOST, 443)):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.SERVER_ADDR = SERVER_ADDR

        self.sock = ssl.wrap_socket(self.s, certfile = APPLICATION['ssl_certificate'], keyfile=APPLICATION['ssl_certificate_key'], server_side = True)
        self.sock.bind(SERVER_ADDR)
        
        self.sock.listen(LISTEN_QUEUE_SIZE)
        
        self.application = application
        if application:
            self.ENABLE_VIRTUALHOST = False
        else:
            self.ENABLE_VIRTUALHOST = True
        
        tmp_regex = '|'.join(STATIC_FILE_SUFFIX) + '$'
        self.STATIC_FILE_REGEX = re.compile(tmp_regex)

        self.lock = threading.Lock()

    def get_environ(self):
        env = super(https_server, self).get_environ()
        env['wsgi.url_scheme'] = 'https'
        return env