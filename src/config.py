
from workflow import ICON_ACCOUNT, ICON_EJECT, ICON_WARNING, ICON_SYNC, ICON_CLOCK

CLIENT_ID = '978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com'
CLIENT_SECRET = 'rty2NIATZfWFWSDX-XPs2usX'
SCOPE = 'https://www.googleapis.com/auth/drive.readonly'
REDIRECT_URI = 'http://127.0.0.1:1337'

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth?scope=%(scope)s&redirect_uri=%(redirect_uri)s&response_type=code&client_id=%(client_id)s&access_type=offline&approval_prompt=force' % {'scope' : SCOPE, 'redirect_uri' : REDIRECT_URI, 'client_id' : CLIENT_ID}

TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'
FILES_URL = 'https://www.googleapis.com/drive/v2/files?maxResults=1000&q=mimeType%3D%22application%2Fvnd.google-apps.document%22+or+mimeType%3D%22application%2Fvnd.google-apps.spreadsheet%22+or+mimeType%3D%22application%2Fvnd.google-apps.presentation%22&fields=items'

CACHE_MAX_AGE = 60*60*24*30 # cache set to 1 month

SETTINGS = {
    'LOGIN' : {
        'title' : 'Login',
        'autocomplete' : '> Login',
        'arg' : 'login',
        'icon' : ICON_ACCOUNT
    },
    'LOGOUT' : {
        'title' : 'Logout',
        'autocomplete' : '> Logout',
        'arg' : 'logout',
        'icon' : ICON_EJECT
    },
    'CLEAR_CACHE' : {
        'title' : 'Clear cache',
        'autocomplete' : '> Clear cache',
        'arg' : 'clear',
        'icon' : ICON_SYNC
    },
    'SET_CACHE' : {
        'title' : 'Set cache length %s',
        'autocomplete' : '> Set cache length ',
        'arg' : 'set%s',
        'icon' : ICON_CLOCK
    }
}

OPTIONS = [
    {
        'title' : 'Search Google Drive',
        'autocomplete' : None
    },
    {
        'title' : 'Type ">" for Settings',
        'autocomplete' : '> '
    }
]

ERRORS = {
    'ConnectionError' : {
        'title' : 'Error with connection',
        'icon' : ICON_WARNING,
        'arg' : None,
        'valid' : False,
        'subtitle' : None
    },
    'InvalidOption' : {
        'title' : 'Invalid option',
        'icon' : ICON_WARNING,
        'arg' : None,
        'valid' : False,
        'subtitle' : None
    },
    'PasswordNotFound' : {
        'title' : 'Account not found, please login',
        'icon' : ICON_WARNING,
        'arg' : 'login',
        'subtitle' : 'Click to login',
        'valid' : True
    }
}

