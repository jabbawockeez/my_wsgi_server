# WSGI server configurations

# host and port
HOST = '0.0.0.0'
PORT = 80

# socket listen queue size
LISTEN_QUEUE_SIZE = 200

# callable application
APPLICATION = {
        'module_path' : 'client/blog',         # module path
        'module_name' : 'blog',            # module name
        'app_name' : 'app',                    # application name
        # 'ssl_certificate' : 'server.crt',
        # 'ssl_certificate_key' : 'server.key',
    }

# static file suffix
STATIC_FILE_SUFFIX = [
        '.html',
        '.js',
        '.css',
        '.jpg',
        '.txt',
        'ico', 
    ]
    
# directory index file
INDEX = ['index.html', ]

# log file
ACCESS_LOG = 'logs/access_log.txt'
ERROR_LOG = 'logs/error_log.txt'

# log format
ACCESS_LOG_FORMAT = [
        # 'host', 
        # 'username', 
        # 'auth-username', 
        # 'timestamp', 
        # 'request-line', 
        # 'response-code', 
        # 'response-size', 
        'Remote-Host', 
        'Username', 
        'Auth-Username', 
        'Date', 
        'Request-Line', 
        'Response-Code', 
        'Content-Length',
    ]
    
# ERROR_LOG_FORMAT = [
#         'Remote-Host', 
#         'Username', 
#         'Auth-Username', 
#         'Date', 
#         'Request-Line', 
#         'Response-Code', 
#         'Content-Length',
#     ]
    
# http Date header GMT time format
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

    
# virtual hosts
# if the APPLICATION is set, the VIRTUALHOST will not make sense
VIRTUALHOST = {
    'www.mytodolist.com': 
    {
        'APPLICATION' : 
        {
            'module_path' : 'client/todolist',       # module path
            'module_name' : 'todo',                    # module name
            'app_name' : 'app'                      # application name
        },
    }, 

    'www.myblog.com': 
    {
        'APPLICATION' : 
        {
            'module_path' : 'client/blog',       # module path
            'module_name' : 'blog',                    # module name
            'app_name' : 'app'                      # application name
        },
    }, 

    'www.mydj.com' :
    {
        'APPLICATION' : 
        {
            'module_path' : 'client/djangoapp/mysite/mysite',    # module path
            'module_name' : 'wsgi',                                # module name
            'app_name' : 'application'                         # application name
        },
    },

    'www.mytornado.com' :
    {
        'APPLICATION' : 
        {
            'module_path' : 'client',                   # module path
            'module_name' : 'tornadoapp',            # module name
            'app_name' : 'application'                 # application name
        },
    },
}