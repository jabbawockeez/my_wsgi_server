#!/usr/bin/env python

# tornado imports
import tornado.wsgi
import tornado.ioloop

# local imports
import routers
print '--------------------'
import config
import uimodules
import os
from database import db
from model import Tag, Post

settings = dict(
    debug=config.DEBUG,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    login_url="/admin/login",
    cookie_secret=config.COOKIE_SECRET,
    ui_modules=uimodules
)


class PaaSApplication(tornado.wsgi.WSGIApplication):

    """the main application"""

    def __init__(self):
        db.create_tables()
        self.tags = []
        self.recent_posts = []
        super(PaaSApplication, self).__init__(
            handlers=routers.route,
            **settings)
        self.flash_cache()

    def flash_cache(self):
        session = db.Session()
        self.tags = session.query(Tag).all()
        self.recent_posts = session.\
            query(Post.title).order_by(Post.post_time.desc())[:5]
        session.close()


class Application(tornado.web.Application):

    def __init__(self):
        self.tags = []
        self.recent_posts = []
        super(Application, self).__init__(
            handlers=routers.route,
            **settings)
        self.flash_cache()

    def flash_cache(self):
        session = db.Session()
        self.tags = session.query(Tag).all()
        self.recent_posts = session.\
            query(Post.title).order_by(Post.post_time.desc())[:5]
        session.close()


tornado_app = Application()

application = tornado.wsgi.WSGIAdapter(tornado_app)

# if "SERVER_SOFTWARE" in os.environ:
#     try:
#         import sae
#         application = sae.create_wsgi_app(PaaSApplication())
#     except:
#         from bae.core.wsgi import WSGIApplication
#         application = WSGIApplication(PaaSApplication())
# else:
#     application = Application()
#     application.listen(8888)
#     tornado.ioloop.IOLoop.instance().start()
