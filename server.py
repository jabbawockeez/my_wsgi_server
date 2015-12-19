#!/usr/bin/env python
#encoding: utf-8

import os
import sys
import StringIO
import datetime
import socket

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


class WSGIServer(object):
    
    def __init__(self, application, SERVER_ADDR = ('localhost', 8080)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.SERVER_ADDR = SERVER_ADDR
        self.sock.bind(SERVER_ADDR)
        
        LISTEN_QUEUE_SIZE = 3
        self.sock.listen(LISTEN_QUEUE_SIZE)
        
        self.set_app(application)
    
    def set_app(self, application):
        self.application = application
    
    def parse_request(self, orig_request):
        request_line = orig_request.splitlines()[0]
        print request_line
        
        self.request_method, \
        self.request_path, \
        self.request_version = request_line.split()
    
    def get_environ(self):
        env = dict()
        
        # set required CGI variables
        env['REQUEST_METHOD']  = self.request_method
        env['PATH_INFO']       = self.request_path
        env['SERVER_PROTOCOL'] = self.request_version
        env['SERVER_NAME'], env['SERVER_PORT'] = self.SERVER_ADDR
        
        # set required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO.StringIO(self.orig_request)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        
        return env
    
    def start_response(self, status, response_headers, exc_info = None):
        date = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        server_headers = [
            ('Date' , date),
            ('Server' , 'MyWSGIServer 1.0')
            ]
        
        self.headers = [status, server_headers + response_headers]
    
    def finish_response(self, result):
        #----------- code in start_response ---------
        """
        date = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        server_headers = [
            ('Date' , date),
            ('Server' , 'MyWSGIServer 1.0')
            ]
            
        status = "200 OK"
        response_headers = []
        self.headers = [status, server_headers + response_headers]
        """
        #--------------------------------------------
        
        status, headers = self.headers
        
        response = 'HTTP/1.1 %s\r\n' % status
        
        for k, w in headers:
            response += '%s: %s\r\n' % (k, w)
            
        response += '\r\n'

        for data in result:
            response += data

        self.client_sock.sendall(response)
        self.client_sock.close()
    
    def handle_one_request(self):
        self.orig_request = self.client_sock.recv(1024)
        
        print self.orig_request
        self.parse_request(self.orig_request)
        
        env = self.get_environ()
        
        # call the application callable and get back the HTTP body
        result = self.application(env, self.start_response)
        
        # construct a response and send it back to the client
        self.finish_response(result)

    
    def serve_forever(self):
        while True:
            print 'listening......'
            self.client_sock = self.sock.accept()[0]
            self.handle_one_request()

def make_server(application):
    server = WSGIServer(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    server = make_server(application)
    server.serve_forever()
    