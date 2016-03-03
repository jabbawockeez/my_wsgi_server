#!/usr/bin/env python
#encoding: utf-8

import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect(('192.168.80.135', 8080))
    request = 'GET / HTTP/1.1' * 1000
    sock.sendall(request)
    # resp = sock.recv(1024)
    # print resp
    
    sock.close()
