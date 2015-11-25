
from workflow import ICON_ACCOUNT, ICON_EJECT, ICON_WARNING, ICON_SYNC, ICON_CLOCK

CLIENT_ID = '978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com'
CLIENT_SECRET = 'rty2NIATZfWFWSDX-XPs2usX'
SCOPE = 'https://www.googleapis.com/auth/drive.readonly'
REDIRECT_URI = 'http://127.0.0.1:1337'

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth?scope=%s&redirect_uri=%s&response_type=code&client_id=%s&access_type=offline&approval_prompt=force' % (SCOPE, REDIRECT_URI, CLIENT_ID)

TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'
FILES_URL = 'https://www.googleapis.com/drive/v2/files?orderBy=lastViewedByMeDate+desc&fields=items'

CACHE_MAX_AGE = 60*60 # cache set to 1 hour

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
        'title' : 'Search Google Drive'
    },
    {
        'title' : 'Type ">" for Settings'
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

