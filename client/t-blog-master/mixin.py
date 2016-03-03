import tornado.web
from model import Post, Category, Tag
from sqlalchemy import func
from config import site_options


class BaseMixin(object):

    def _get_limit_offset(self, page):
        offset = (page - 1) * site_options["index_page_size"]
        limit = site_options["index_page_size"]
        return limit, offset

    def _get_start_end(self, page, page_size):
        start = (page - 1) * page_size
        end = page * page_size
        return start, end

    def _add_filters(self, T, rc, **kwargs):
        if "in_" in kwargs:
            for (key, value) in kwargs["in_"]:
                rc = rc.filter(getattr(T, key).in_(value))
        for (key, value) in kwargs.items():
            if not hasattr(T, key):
                continue
            rc = rc.filter(getattr(T, key) == value)
        if "limit" in kwargs:
            rc = rc.limit(kwargs["limit"])
        if "offset" in kwargs:
            rc = rc.offset(kwargs["offset"])
        return rc

    def get_one(self, T, **kwargs):
        rc = self.db.query(T)
        rc = self._add_filters(T, rc, **kwargs)
        try:
            return rc.one()
        except:
            raise tornado.web.HTTPError(404)

    def get_model_list(self, T, *cols, **kwargs):
        if cols:
            query_list = [getattr(T, col)
                          for col in cols if hasattr(T, col)]
            rc = self.db.query(*query_list)
        else:
            rc = self.db.query(T)
        rc = self._add_filters(T, rc, **kwargs)
        return rc.all()

    def count(self, T, **kwargs):
        rc = self.db.query(T)
        rc = self._add_filters(T, rc, **kwargs)
        return rc.count()

    def insert(self, model):
        self.db.add(model)
        self.db.commit()

    def insert_many(self, models):
        self.db.add_all(models)
        self.db.commit()

    def update(self, T, data, **kwargs):
        rc = self.db.query(T)
        rc = self._add_filters(T, rc, **kwargs)
        rc.update(data)
        self.db.commit()

    def delete(self, T, **kwargs):
        rc = self.db.query(T)
        rc = rc._add_filters(T, rc, **kwargs)
        rc.delete()
        self.db.commit()


class PostMixin(object):

    def _do_join(self, rc, category_name, tag_name):
        if category_name:
            rc = rc.join(Post.category)
            rc = rc.filter(Category.name == category_name)
        if tag_name:
            rc = rc.join(Post.tags)
            rc = rc.filter(Tag.name == tag_name)
        return rc

    def count_posts(self, category_name=None, tag_name=None):
        my_query = self.db.query(Post)
        my_query = self._do_join(my_query, category_name, tag_name)
        return my_query.count()

    def get_posts(self, category_name=None, tag_name=None, page=1):
        my_query = self.db.query(Post)
        my_query = self._do_join(my_query, category_name, tag_name)
        start, end = self._get_start_end(
            page, site_options["index_page_size"])
        return my_query.order_by(Post.id.desc())[start:end]

    def get_recent_posts(self):
        return self.db.\
            query(Post.id, Post.title).\
            order_by(Post.post_time.desc())[:5]

    def get_headers(self, category_id=None, page=1):
        my_query = self.db.query(
            Post.id,
            Post.title,
            Category.name,
            Post.post_time).join(Post.category)
        if category_id:
            my_query = my_query.filter(Post.category_id == category_id)
        start, end = self._get_start_end(
            page, site_options["archive_page_size"])
        return my_query.order_by(Post.id.desc())[start: end]

    def get_category_info(self):
        return self.db.query(Category.name, func.count(Post.id)).\
            join(Post.category).\
            group_by(Post.category_id).\
            all()
