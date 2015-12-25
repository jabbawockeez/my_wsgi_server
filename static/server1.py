#!/usr/bin/env python

import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 8080))
sock.listen(5)

def func(client_sock):

    request = client_sock.recv(1024)

    print '--------------------'
    print request
    print '--------------------'
    print len(request)

    client_sock.send('test')
    client_sock.close()

    # print threading.currentThread()

while True:
    print 'listening'
    client_sock, client_ip = sock.accept()

    t = threading.Thread(target = func, args = (client_sock, ))
    t.start()

    # print threading.enumerate()
