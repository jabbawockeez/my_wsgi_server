# WSGI server configurations

# host and port
HOST = 'localhost'
PORT = 8080


# callable application
APPLICATION = [
        'client',       # module path
        'webpydemo',   # module name
        'app'           # application name
    ]

# static file suffix
STATIC_FILE_SUFFIX = [
        '.html',
        '.js',
        '.css',
        '.jpg',
        '.txt',
    ]
    
# the 
    
# directory index file
INDEX = ['index.html', ]

# log file
ACCESS_LOG = 'logs/access_log.txt'
ERROR_LOG = 'logs/error_log.txt'

# log format
ACCESS_LOG_FORMAT = [
        'remotehost', 
        'usernam', 
        'auth-username', 
        'timestamp', 
        'request-line', 
        'response-code', 
        'response-size', 
    ]
    
ERROR_LOG_FORMAT = [
        'remotehost', 
        'usernam', 
        'auth-username', 
        'timestamp', 
        'request-line', 
        'response-code', 
        'response-size', 
    ]
    
# http Date header GMT time format
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
