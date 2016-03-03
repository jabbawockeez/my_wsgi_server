from tornado.web import authenticated
from . import BaseHandler, flash_cache
from model import Tag


class IndexHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("tag.html", tags=self.get_model_list(Tag))

    @authenticated
    @flash_cache
    def post(self):
        tag_name = self.get_argument("name")
        self.insert(Tag(tag_name))
        self.redirect("/admin/tags")


class EditHandler(BaseHandler):

    @authenticated
    def get(self, tag_id):
        self.render(
            "tag_edit.html",
            tag=self.get_one(Tag, **dict(id=int(tag_id)))
        )

    @authenticated
    @flash_cache
    def post(self, tag_id):
        self.update_tag(int(tag_id), self.get_argument("name").strip())
        self.redirect("/admin/tags")
