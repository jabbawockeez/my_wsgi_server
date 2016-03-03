import tornado.web
from database import db
from config import site_options
from mixin import BaseMixin, PostMixin


class BaseHandler(tornado.web.RequestHandler, BaseMixin, PostMixin):
    def initialize(self):
        self.db = db.Session()
        self.tags = self.application.tags
        self.recent_posts = self.application.recent_posts
        self.flash_cache = self.application.flash_cache

    def get_current_user(self):
        return self.get_secure_cookie("status")

    def render(self, template_name, **kwargs):
        if not self.request.path.startswith("/admin"):
            kwargs["tags"] = self.tags
            kwargs["recent_posts"] = self.recent_posts
            kwargs["links"] = [dict(name="test", url="#"), ]
            template_name = site_options["theme"] + '/' + template_name
        super(BaseHandler, self).render(
            template_name,
            site_options=site_options,
            **kwargs
        ) 

    def on_finish(self):
        self.db.close()


def flash_cache(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        args[0].application.flash_cache()
    return wrapper