from . import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        self.render("about.html")
