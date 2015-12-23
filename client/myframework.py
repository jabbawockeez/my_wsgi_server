def run_application(application):

    headers_set = []

    environ = {}
 
    def start_response(status, response_headers, exc_info=None):
        headers_set[:] = [status, response_headers]

    result = application(environ, start_response)
 
def app(environ, start_response):
    """A barebones WSGI app."""
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello world!']
 
run_application(app)