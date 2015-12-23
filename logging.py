# Define two functions write to log files.

from settings import *

import os
import time
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

# class Log(dict):
#     def __init__(self, **kwargs):
#         pass


def access_logging(request, response, client_ip):

    request, response = trim_info(request, response)

    # info is a dict that contains all the informations to be logged
    info = {}

    request_lines = request.splitlines()
    response_lines = response.splitlines()

    info['Request-Line'] = request_lines[0]
    info['Response-Code'] = response_lines[0].split()[1]
    print type(client_ip)
    info['Remote-Host'] = client_ip[0]

    all_info = request_lines[1 : ] + response_lines[1 : ]

    print '-----------------------------logging--------------------------------'
    print all_info
    print '-----------------------------logging--------------------------------'

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
        print info[i]
        if i == 'Date':
            msg += '[%s] ' % info[i]
        elif i == 'Request-Line':
            msg += '"%s" ' % info[i]
        else:
            msg += '%s ' % info[i]


    # if the log directory does not exists, then create it
    if not os.path.exists(os.path.dirname(ACCESS_LOG)):
        os.mkdir(os.path.dirname(ACCESS_LOG))

    print msg
    with open(ACCESS_LOG, 'a') as f:
        f.write(msg)


def error_logging(request, response, client_ip):
    print '-----------------------------logging error--------------------------------'


def trim_info(request, response):
    pos = request.find('\n\n')
    new_request = request[ : pos]
    pos = response.find('\r\n\r\n')
    new_response = response[ : pos]

    return new_request, new_response
