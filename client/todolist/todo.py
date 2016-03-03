#!/usr/bin/env python

import web
import model

import os

### Url mappings

urls = (
    '/', 'Index',
    '/del/(\d+)', 'Delete',
    '/.*', 'Error',
)


### Templates
render = web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'), base='base')


class Index:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            description="I need to:"),
        web.form.Button('Add todo'),
    )

    def GET(self):
        todos = model.get_todos()
        form = self.form()
        return render.index(todos, form)

    def POST(self):
        form = self.form()
        if not form.validates():
            todos = model.get_todos()
            return render.index(todos, form)
        model.new_todo(form.d.title)
        raise web.seeother('/')



class Delete:

    def POST(self, id):
        id = int(id)
        model.del_todo(id)
        raise web.seeother('/')

class Error:
        def GET(self):
            return "<h1>Page Not Found</h1>"
        def POST(self):
            self.GET()

app = web.application(urls, globals()).wsgifunc()

if __name__ == '__main__':
    app.run()
