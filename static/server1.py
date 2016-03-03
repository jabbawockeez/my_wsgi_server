#!/usr/bin/env python

import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 443))
sock.listen(5)

while True:
    print 'listening'
    client_sock, client_ip = sock.accept()

    orig_request = ''

    # while True:
        # req = ''
    req = client_sock.recv(1024)
    print req

        # orig_request += req

        # client_sock.settimeout(2)

        # if len(req) < 1024:
        #     break

    print '------------------------------------------------------------------------'
    # print orig_request
