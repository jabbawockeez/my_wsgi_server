# Define two functions write to log files.

from mysettings import *
import mydebug

import os
import time
import datetime
import re


# response
# HTTP/1.1 200 OK
# Content-Type: text/html
# Content-Length: 218
# Date: Wed, 23 Dec 2015 07:15:19 GMT

# request
# GET /index.html HTTP/1.1
# Host: 192.168.80.135:8080

# log example
# 209.1.32.44 - - [03/Oct/1999:14:16:00 -0400] "GET / HTTP/1.0" 200 1024
# 209.1.32.44 - - [23/Dec/2015:16:07:43] "GET /index.html HTTP/1.1" 200 218 
# http-guide.com - dg [03/Oct/1999:14:16:32 -0400] "GET / HTTP/1.0" 200 477

# Host, Username, Auth-Username, Date, Request-Line, Response-Code, Content-Length


def access_logging(request, response, client_ip, lock):

    if not (request and response and client_ip):
        return

    request, response = trim_info(request, response)

    # info is a dict that contains all the informations to be logged
    info = {}

    request_lines = request.splitlines()
    response_lines = response.splitlines()

    info['Request-Line'] = request_lines[0]
    info['Response-Code'] = response_lines[0].split()[1]
    info['Remote-Host'] = client_ip[0]

    all_info = request_lines[1 : ] + response_lines[1 : ]

    for i in all_info:
        try:
            k, w = i.split(':', 1)
            info[k] = w.strip()
        except:
            continue

    for i in ACCESS_LOG_FORMAT:
        if i not in info:
            info[i] = '-'

    # format the Date
    timeArray = time.strptime(info['Date'], GMT_FORMAT)
    info['Date'] = time.strftime("%d/%b/%Y:%H:%M:%S", timeArray)

    msg = ''

    for i in ACCESS_LOG_FORMAT:
        if i == 'Date':
            msg += '[%s] ' % info[i]
        elif i == 'Request-Line':
            msg += '"%s" ' % info[i]
        else:
            msg += '%s ' % info[i]
    msg += '\n'


    # if the log directory does not exists, then create it
    if not os.path.exists(os.path.dirname(ACCESS_LOG)):
        os.mkdir(os.path.dirname(ACCESS_LOG))

    mydebug.output('access_log', msg)

    with lock:
        with open(ACCESS_LOG, 'a+') as f:
            # mydebug.output('before write access file', f.read())
            f.read()
            # f.seek(2, 0)
            f.write(msg)
            # f.seek(0)
            # mydebug.output('after write access file', f.read())

# [Wed Oct 11 14:32:52 2000] [error] [client 127.0.0.1] client denied by server configuration: /export/ap/htdocs/test

def error_logging(error_info, lock):

    if not error_info:
        return

    # format the Date
    date = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S")

    msg = '[%s] %s\n' % (date, error_info)

    # if the log directory does not exists, then create it
    if not os.path.exists(os.path.dirname(ERROR_LOG)):
        os.mkdir(os.path.dirname(ERROR_LOG))

    mydebug.output('error_log', msg)

    with lock:
        with open(ERROR_LOG, 'a+') as f:
            # mydebug.output('before write error file', f.read())
            f.seek(2)
            f.write(msg)
            # f.seek(0)
            # mydebug.output('after write error file', f.read())



def trim_info(request, response):
    pos = request.find('\n\n')
    new_request = request[ : pos]
    pos = response.find('\r\n\r\n')
    new_response = response[ : pos]

    mydebug.output('trimmed request', new_request)
    mydebug.output('trimmed response', new_response)

    return new_request, new_response
