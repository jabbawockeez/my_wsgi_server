#!/usr/bin/env python

# import tornado.ioloop
import tornado.web
import tornado.wsgi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>tornado</h1>")

# application = tornado.web.Application([
#                 (r"/", MainHandler),
# ])

tornado_app = tornado.web.Application([
                (r"/", MainHandler),
])
application = tornado.wsgi.WSGIAdapter(tornado_app)

# if __name__ == "__main__":
#     application.listen(8080)
#     tornado.ioloop.IOLoop.instance().start()