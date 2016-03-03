from . import BaseHandler, flash_cache
from tornado.web import authenticated
from model import Category


class IndexHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("category.html", categories=self.get_model_list(Category))

    @authenticated
    @flash_cache
    def post(self):
        self.insert(Category(self.get_argument("name")))
        self.redirect("/admin/categories")


class EditHandler(BaseHandler):

    @authenticated
    def get(self, category_id):
        self.render(
            "category_edit.html",
            category=self.get_one(Category, **dict(id=int(category_id)))
        )

    @authenticated
    @flash_cache
    def post(self, category_id):
        self.update(
            Category,
            dict(name=self.get_argument("name")),
            dict(id=category_id)
        )
        self.redirect("/admin/categories")


class DeleteHandler(BaseHandler):

    @authenticated
    def get(self, category_id):
        self.render("category_delete.html",
                    self.get_one(Category, **dict(id=int(category_id))))

    @authenticated
    @flash_cache
    def delete(self):
        self.delete(Category, **dict(id=int(self.get_argument("id"))))
        self.redirect("/admin/categories")
