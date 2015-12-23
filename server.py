#!/usr/bin/env python
#encoding: utf-8

import os
import sys
import StringIO
import datetime
import socket
import time
import threading
import re

from settings import *


class WSGIServer(object):
    
    def __init__(self, application, SERVER_ADDR = (HOST, PORT)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.SERVER_ADDR = SERVER_ADDR
        self.sock.bind(SERVER_ADDR)
        
        LISTEN_QUEUE_SIZE = 3
        self.sock.listen(LISTEN_QUEUE_SIZE)
        
        # set the callable application
        self.set_app(application)
        
        # compile the regexp object that will match
        # the defined static file suffix
        tmp_regex = '|'.join(STATIC_FILE_SUFFIX) + '$'
        self.STATIC_FILE_REGEX = re.compile(tmp_regex)
        
    
    def set_app(self, application):
        self.application = application
    
    def parse_request(self, orig_request):
        request_line = orig_request.splitlines()[0]
        #print request_line
        
        self.request_method, \
        self.request_path, \
        self.request_version = request_line.split()
        print 'request path', self.request_path
    
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
        
        self.headers = [status, response_headers]
    
    def finish_response(self, result, client_sock):
        # generate the GMT time format
        date = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        
        server_headers = [
            ('Date' , date),
            ('Server' , 'MyWSGIServer/1.0')
            ]
        
        status, headers = self.headers
        headers += server_headers
        
        response = 'HTTP/1.1 %s\r\n' % status 
        
        for k, w in headers:
            response += '%s: %s\r\n' % (k, w)
            
        response += '\r\n'

        for data in result:
            response += data

        #time.sleep(10)
        client_sock.sendall(response)
        client_sock.close()
        
        # write message to log file
        # if status == '200':
        #     access_logging()
        # else:
        #     error_logging()
    
    def handle_one_request(self, client_sock, client_ip):
        self.orig_request = client_sock.recv(1024)
        
        print self.orig_request
        self.parse_request(self.orig_request)
        
        # see if the client requests a static file
        # if any STATIC_FILE_SUFFIX in the request_path,
        # then serve a file in the static directory
        matched = self.STATIC_FILE_REGEX.search(self.request_path)
        if matched:
            result = self.serve_static_file()
        else:
            env = self.get_environ()
            
            # call the application callable and get back the HTTP body
            result = self.application(env, self.start_response)
        
        # construct a response and send it back to the client
        self.finish_response(result, client_sock)

    
    def serve_static_file(self):
        fullname = 'static' + self.request_path
        
        try:
            with open(fullname, 'rb') as f:
                content =  f.read()
        except Exception as e:
            print e
            # status = '404 Not Found'
            # response_headers = []
            with open('static/404.html', 'r') as f:
                content =  f.read()
            self.start_response('404 NOT FOUND', [])
        else:
            # status = '200 OK'
            # response_headers = [('Content-Type', 'text/html')]
            self.start_response('200 OK', \
                [('Content-Type', 'text/html'), 
                ('Content-Length', len(content))])
        return content
    
    def serve_forever(self):
        
        while True:
            print 'listening......'
            client_sock, client_ip = self.sock.accept()
            #self.handle_one_request()
            t = threading.Thread(target = self.handle_one_request, \
                args = (client_sock, client_ip))
            t.start()


def make_server(application):
    server = WSGIServer(application)
    return server

if __name__ == '__main__':
    try:
        ( module_path, 
        module_name, 
        app_name ) = APPLICATION
        
        sys.path.insert(0, module_path)
        
        module = __import__(module_name)
        application = getattr(module, app_name)
    
    except Exception as e:
        print e
        print "Failed to import callable application %s/%s:%s" %\
            (module_path, module_name, app_name)
        sys.exit()
        
    server = make_server(application)
    server.serve_forever()

    
    