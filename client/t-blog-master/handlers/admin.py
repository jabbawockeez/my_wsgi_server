from tornado.web import authenticated, RequestHandler
from . import BaseHandler
from config import site_options


class IndexHandler(BaseHandler):
    @authenticated
    def get(self):
        category_info = self.get_category_info()
        post_count = 0
        for item in category_info:
            post_count = post_count + item[1]
        self.render(
            "admin.html",
            category_info=category_info,
            post_count=post_count)


class LoginHandler(RequestHandler):
    def get(self):
        if self.get_secure_cookie("status"):
            self.redirect("/admin")
            return
        error_msg = self.get_argument("e", None)
        self.render("login.html", error_msg=error_msg)

    def post(self):
        if self.get_argument("pass", None) == site_options["password"]:
            self.set_secure_cookie("status", "Authenticated!")
            self.redirect("/admin")
        else:
            self.redirect("/admin/login?e=1")


class LogoutHandler(RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")
