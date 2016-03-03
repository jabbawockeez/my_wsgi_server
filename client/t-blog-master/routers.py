from handlers import index, post, admin, category, tag, about

#system routes
route = [
    (r"/", index.IndexHandler),
    (r"/archive", index.ArchiveHandler),
    (r"/post/([^/]+)", post.ShowHandler),
    (r"/admin", admin.IndexHandler),
    (r"/admin/remote", post.RemoteHandler),
    (r"/admin/login", admin.LoginHandler),
    (r"/admin/logout", admin.LogoutHandler),
    (r"/admin/add_post", post.AddHandler),
    (r"/admin/posts", post.ListHandler),
    (r"/admin/post/edit/([0-9]+)", post.EditHandler),
    (r"/admin/post/delete/([0-9]+)", post.DeleteHandler),
    (r"/admin/categories", category.IndexHandler),
    (r"/admin/tags", tag.IndexHandler),
    (r"/admin/category/edit/([0-9]+)", category.EditHandler),
    (r"/admin/category/delete/([0-9]+)", category.DeleteHandler),
    (r"/admin/tag/edit/([0-9]+)", tag.EditHandler),

    (r"/about", about.IndexHandler)
]
