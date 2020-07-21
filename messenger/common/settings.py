MAX_CONNECTIONS = 5
DEFAULT_USER = 'Guest'
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 7777
ENCODING = 'utf-8'
MAX_PACKAGE = 1024
DEFAULT_ACCOUNT = 'Guest'
LOGGING_LEVEL = 'DEBUG'
MAX_TRYING = 10

RESPONSE = 'response'
SERVICE = 'service'
SERVER = 'server'
ACTION = 'action'
HELP = 'help'
ERROR = 'error'
VALUE = 'value'
PRESENCE = 'presence'
MESSAGE = 'message'
ADDRESS = 'address'
NAME = 'name'
EXIT = 'exit'
ALL = 'всем'
TO = 'to'
RESPONSE_409 = {ACTION: PRESENCE,
                RESPONSE: 409,
                ERROR: 'Пользователь с таким именем уже существует'}
RESPONSE_200 = {ACTION: PRESENCE,
                RESPONSE: 200,
                MESSAGE: 'ok'}
RESPONSE_400 = {ACTION: SERVICE,
                RESPONSE: 400,
                MESSAGE: 'неправильный JSON-объект'}
