import web
import time
        
urls = (
    '/', 'hello',
    '/(.*)', 'error',
)

class hello:        
    def GET(self):
        return '<h1>Hello from web.py</h1>'

class error:
    def GET(self, obj):
        #raise web.notfound()
        return "%s not found" % obj

def notfound():  
    return web.notfound("Sorry, the page you were looking for was not found.........")  

    #return web.notfound(render.notfound())  
    #return web.notfound(str(render.notfound()))  
  
def internalerror():  
    return web.internalerror("Bad, bad server. No donut for you.")  
        
        
app = web.application(urls, globals()).wsgifunc()
app.notfound = notfound  
app.internalerror = internalerror

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