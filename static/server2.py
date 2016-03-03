#!/usr/bin/env python

import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 80))
sock.listen(5)

# def func(i):

#     with open('logs.txt', 'a') as f:
#         f.write(str(i) + '\n')
#     print threading.currentThread()

# for i in range(51):
#     print i
#     t = threading.Thread(target = func, args = (i, ))
#     t.start()

    # print threading.enumerate()
