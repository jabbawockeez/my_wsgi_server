from pyramid.config import Configurator
from pyramid.response import Response
 
def hello_world(request):
    return Response(
        '<p>Hello world from Pyramid!n</p>',
        content_type='text/html',
    )
 
config = Configurator()
config.add_route('hello', '/hello')
config.add_view(hello_world, route_name='hello')
app = config.make_wsgi_app()