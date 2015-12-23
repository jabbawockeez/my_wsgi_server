import web
import time
        
urls = (
    '/', 'hello'
)

class hello:        
    def GET(self):
        return 'Hello from web.py'
        
app = web.application(urls, globals()).wsgifunc()


# class myapp(web.application):
#     def __init__(self, urls = urls, globals = globals()):
#         web.application.__init__(self, urls, globals)
        
#     def __call__(self, env, start_response):
#         request_path = env['PATH_INFO']
        
#         if request_path == '/':
#             response = "<h1>hello from web.py in path /</h1>"
            
#         else:
#             response = "<h1>hello from web.py in other path</h1>"
            
#         start_response('200 OK', [('Content-Type', 'text/html')])
        
#         return response

        
# app = myapp()