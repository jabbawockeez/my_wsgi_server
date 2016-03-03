import tornado.web
from tornado.web import authenticated
from . import BaseHandler, flash_cache
from mixin import PostMixin
from model import Post, Tag, Category
from config import site_options

from datetime import datetime
import hashlib
from urllib import unquote, quote


class AddHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render(
            "post_add.html",
            tags=self.get_model_list(Tag),
            categories=self.get_model_list(Category)
        )

    @authenticated
    @flash_cache
    def post(self):
        my_post = Post()
        my_post.title = self.get_argument("title")
        my_post.content = self.get_argument("content")
        my_post.category_id = int(self.get_argument("category"))
        my_post.tags = self.get_model_list(
            Tag,
            **dict(in_=[("id", self.get_arguments("tags"))])
        )
        my_post.post_time = datetime.now()
        self.insert(my_post)
        self.redirect("/admin/posts")


class ListHandler(BaseHandler):

    @authenticated
    def get(self):
        category_id = self.get_argument("cate", None)
        if category_id:
            category_id = int(category_id)
        self.render("post_list.html", headers=self.get_headers(category_id))


class ShowHandler(BaseHandler, PostMixin):
    def get(self, title):
        title = unquote(title.encode('utf-8')).decode('utf-8')
        article = self.get_one(Post, title=title)
        if article:
            self.render("post.html", article=article)
        else:
            raise tornado.web.HTTPError(404)


class EditHandler(BaseHandler):

    @authenticated
    def get(self, id):
        my_post = self.get_one(Post, **dict(id=id))
        selected_tags = [i.id for i in my_post.tags]
        self.render(
            "post_edit.html",
            post=my_post,
            tags=self.get_model_list(Tag),
            selected_tags=selected_tags,
            categories=self.get_model_list(Category)
        )

    @authenticated
    @flash_cache
    def post(self, post_id):
        my_post = self.get_one(Post, **dict(id=post_id))
        my_post.title = self.get_argument("title")
        my_post.content = self.get_argument("content")
        my_post.category_id = int(self.get_argument("category"))
        my_post.tags = self.get_model_list(
            Tag,
            **dict(in_=[("id", self.get_arguments("tags"))])
        )
        self.db.commit()
        self.redirect("/admin/posts")


class DeleteHandler(BaseHandler):

    @authenticated
    def get(self, post_id):
        self.render("post_delete.html",
                    post=self.get_one(Post, "id", "title", **dict(id=post_id)))

    @authenticated
    @flash_cache
    def post(self, post_id):
        self.delete(Post, dict(id=int(post_id)))
        self.redirect("/admin/posts")


class RemoteHandler(BaseHandler):
    def post(self):
        password = self.get_argument("password", None)
        md5_password = hashlib.md5(site_options["password"]).hexdigest()
        if not password or password != md5_password:
            raise tornado.web.HTTPError(403)
        category = self.get_argument("category", None)
        tags = self.get_argument("tags", "").split(",")
        content = self.get_argument("content", None)
        print category
        print tags
        print content.encode("utf8")
