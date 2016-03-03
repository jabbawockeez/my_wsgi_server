from . import BaseHandler
from mixin import PostMixin


class IndexHandler(BaseHandler, PostMixin):
    def get(self):
        category = self.get_argument("cate", None)
        tag = self.get_argument("tag", None)
        page = int(self.get_argument("p", 1))
        total = self.count_posts(category, tag)
        posts = self.get_posts(category, tag, page)
        self.render(
            "index.html",
            category=category,
            tag=tag,
            articles=posts,
            total=total,
            current_page=page
        )


class ArchiveHandler(BaseHandler, PostMixin):
    def get(self):
        page = int(self.get_argument("p", 1))
        total = self.count_posts()
        self.render(
            "archive.html",
            articles=self.get_headers(),
            current_page=page,
            total=total
        )
