# WSGI server configurations

# host and port
HOST = '0.0.0.0'
PORT = 8080


# callable application
APPLICATION = [
        'client/blog',               # module path
        'blog',   # module name
        'app'                   # application name
    ]

# static file suffix
STATIC_FILE_SUFFIX = [
        '.html',
        '.js',
        '.css',
        '.jpg',
        '.txt',
        'ico', 
    ]
    
# the 
    
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
