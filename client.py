#!/usr/bin/env python
#encoding: utf-8

import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect(('127.0.0.1', 8080))
    request = 'GET /hello HTTP/1.1'
    sock.send(request)
    resp = sock.recv(1024)
    print resp
    
    sock.close()