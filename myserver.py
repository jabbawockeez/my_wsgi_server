#!/usr/bin/env python
#encoding: utf-8

import os
import sys
import StringIO
import datetime
import socket
import struct
import time
import threading
import re
import multiprocessing
import importlib

import mylogging
from mysettings import *
import mydebug
import myhttps


class WSGIServer(object):
    
    def __init__(self, application = None, SERVER_ADDR = (HOST, PORT)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.SERVER_ADDR = SERVER_ADDR
        self.sock.bind(SERVER_ADDR)
        
        self.sock.listen(LISTEN_QUEUE_SIZE)
        
        # set the callable application
        self.application = application
        if application:
            self.ENABLE_VIRTUALHOST = False
        else:
            self.ENABLE_VIRTUALHOST = True
        
        # compile the regexp object that will match
        # the defined static file suffix
        tmp_regex = '|'.join(STATIC_FILE_SUFFIX) + '$'
        self.STATIC_FILE_REGEX = re.compile(tmp_regex)

        # set a lock to synchronize all threads 
        # self.lock = multiprocessing.Lock()
        self.lock = threading.Lock()
        
    
    def set_app(self, server_name):
        if not self.ENABLE_VIRTUALHOST:
            self.application = APPLICATION['app']
            return
        elif VIRTUALHOST in dir() and server_name not in VIRTUALHOST:
            raise Exception('%s not found!' % server_name)
        # self.application = VIRTUALHOST[server_name]['APPLICATION']['app']
        a = VIRTUALHOST[server_name]['APPLICATION']
        module_fullname = a['module_path'].replace('/', '.') + '.' + a['module_name']
        m = importlib.import_module(module_fullname)
        self.application = getattr(m, a['app_name'])
    
    def parse_request(self, orig_request):
        try:
            request_line = orig_request.splitlines()[0]
            #print request_line
        except Exception as e:
            #raise e
            return
        else:
            self.request_method, \
            self.request_path, \
            self.request_version = request_line.split()

            self.request_path = self.request_path.lower()
    
    def get_environ(self):
        env = dict()
        
        # set required CGI variables
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.request_path
        env['SERVER_PROTOCOL'] = self.request_version
        env['SERVER_NAME'], env['SERVER_PORT'] = self.SERVER_ADDR
        
        # set required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = StringIO.StringIO(self.orig_request.splitlines()[-1])
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False

        # get other request headers
        for i in self.orig_request.splitlines()[1 : -3]:
            if re.match('Content-Length', i):
                env['CONTENT_LENGTH'] = int(i.split(':', 1)[1].strip()) + 1
            elif re.match('Host', i):
                env['HTTP_HOST'] = i.split(':', 1)[1].strip()
        
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

        mydebug.output('response', response)

        # write message to log file
        if not re.match('4|5', status):
            mylogging.access_logging(self.orig_request, response, self.client_ip, self.lock)
        else:
            mylogging.error_logging(status, self.lock)

        #time.sleep(4)
        try:
            client_sock.sendall(response)
            client_sock.close()
        except Exception as e:
            raise e

    def recvall(self, sock, msgLen):
        msg = ""

        h = sock.recv(msgLen)
        msg += h

        mydebug.output('h', h)
        contlen_header = re.search('Content-Length: .*\n', h)
        if not contlen_header:
            return msg

        # get the client's os type, to determin the line seperator of the request headers
        ua = re.search('User-Agent: .*\n', h)
        if -1 != str(ua.group()).find('Windows'):
            linesep = '\r\n'
        else:
            linesep = '\n'
        # linesep = '\r\n\r\n'

        contlen = int(contlen_header.group().split(':')[1])
        mydebug.output('contlen', contlen)

        if contlen > 0:
            try:
                print h.split(linesep * 2)
                bodyRcvd = h.split(linesep * 2)[1]
            except:
                bodyRcvd = ''

            if contlen > len(bodyRcvd):
                msg += sock.recv(contlen - len(bodyRcvd))

        mydebug.output('msg', msg)
        return msg
    
    def handle_one_request(self, client_sock, client_ip):
        # mydebug.output('path', globals())

        self.orig_request = ''

        try:
            self.orig_request = self.recvall(client_sock, 1024)
            # self.orig_request = client_sock.recv(65535)
            # while True:
            #     # req = ''
            #     req = client_sock.recv(1024)
            #     mydebug.output('req', req)

            #     self.orig_request += req
            #     if len(req) < 1024:
            #         break

            if not len(self.orig_request):
                mydebug.output('request error', 'no request data')
                mylogging.error_logging('no request data', self.lock)
                return

            self.client_ip = client_ip
            
            mydebug.output('orig_request', self.orig_request)
            self.parse_request(self.orig_request)

            env = self.get_environ()

        except Exception as e:
            # mydebug.output('exception', e)
            raise e
        
        try:
            self.set_app(env['HTTP_HOST'])
        except Exception as e:
            print e
            result = self.error()
            self.finish_response(result, client_sock)
            return


        # see if the client requests a static file
        # if any STATIC_FILE_SUFFIX in the request_path,
        # then serve a file in the static directory
        matched = self.STATIC_FILE_REGEX.search(self.request_path)
        if matched:
            print 'serving a static file'
            result = self.serve_static_file()
        else:
            print 'sending the request to the application'
            mydebug.output('env', env)
            
            # call the application callable and get back the HTTP body
            result = self.application(env, self.start_response) 
        
        try:
            # construct a response and send it back to the client
            self.finish_response(result, client_sock)
        except Exception, e:
            raise e

        # self.lock.release()

    def error(self):
        with open('static/404.html', 'r') as f:
            content =  f.read()
        self.start_response('404 Not Found', [('Content-Type', 'text/html')])
        return content

    
    def serve_static_file(self):
        fullname = 'static' + self.request_path
        
        try:
            with open(fullname, 'rb') as f:
                content =  f.read()
        except Exception as e:
            print e
            # status = '404 Not Found'
            # response_headers = []
            content = self.error()
        else:
            #if 'jpg' in self.request_path:
            if re.search(r'jpg$', self.request_path):
                doc_type = 'image/jpg'
            elif re.search(r'ico$', self.request_path):
                doc_type = 'image/png'
            elif 'html' in self.request_path:
                doc_type = 'text/html'

            self.start_response('200 OK', \
                [('Content-Type', doc_type), 
                ('Content-Length', len(content))])
        return content
    
    def serve_forever(self):

        while True:
            print 'listening......'
            try:
                client_sock, client_ip = self.sock.accept()
                mydebug.output('client sock', client_sock)
                #self.handle_one_request()
                t = threading.Thread(target = self.handle_one_request, \
                    args = (client_sock, client_ip))
                t.start()
                mydebug.output('current threads', threading.enumerate())
            except Exception as e:
                mydebug.output('exception', e)
                # mylogging.error_logging(str(e))
            finally:
                pass

def make_server(application, use_ssl = False):
    if use_ssl:
        server = myhttps.https_server(application)
    else:
        server = WSGIServer(application)
    return server

def import_app(APPLICATION):

    # sys.path.insert(0, APPLICATION['module_path'])
    # module = __import__(APPLICATION['module_name'])
    module_fullname = APPLICATION['module_path'].replace('/', '.') + '.' + APPLICATION['module_name']
    m = importlib.import_module(module_fullname)
    # m = importlib.import_module(APPLICATION['module_path'])
    # APPLICATION['app'] = getattr(m, APPLICATION['app_name'])

    try:
        APPLICATION['app'] = getattr(m, APPLICATION['app_name'])
    except Exception as e:
        print e
        APPLICATION['app'] = None

    return APPLICATION['app']

if __name__ == '__main__':

    if not ('APPLICATION' in dir() or 'VIRTUALHOST' in dir()):
        print "No application found!"
        sys.exit()

    application = None
    use_ssl = False

    # if the APPLICATION is set, the VIRTUALHOST will not make sense
    if 'APPLICATION' in dir():
        del VIRTUALHOST
        VIRTUALHOST = {}

        try:
            application = import_app(APPLICATION)
            if 'ssl_certificate' in APPLICATION:
                use_ssl = True
        
        except Exception as e:
            print e
            print "Failed to import callable application %s/%s:%s" %\
                tuple([i for i in APPLICATION.itervalues()])
            sys.exit()

    # else:
        # for i in VIRTUALHOST.itervalues():
        #     if not i.has_key('APPLICATION'):
        #         continue

        #     import_app(i['APPLICATION'])

            # for k, v in globals().items():
            #     print k, ' : ', v

    
    server = make_server(application, use_ssl)
    server.serve_forever()


    