import urllib
from workflow import ICON_ACCOUNT, ICON_EJECT, ICON_WARNING, ICON_SYNC, ICON_CLOCK

CLIENT_ID = '978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com'
CLIENT_SECRET = 'rty2NIATZfWFWSDX-XPs2usX'
SCOPE = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.file'
FILTER = urllib.quote("mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet' or mimeType='application/vnd.google-apps.presentation' or mimeType='application/vnd.google-apps.form' or mimeType='application/pdf'")
REDIRECT_URI = 'http://127.0.0.1:1337'

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth?scope=%(scope)s&redirect_uri=%(redirect_uri)s&response_type=code&client_id=%(client_id)s&access_type=offline&approval_prompt=force' % {'scope' : SCOPE, 'redirect_uri' : REDIRECT_URI, 'client_id' : CLIENT_ID}

TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'
FILES_URL = 'https://www.googleapis.com/drive/v2/files?maxResults=1000&q=%(filter)s&fields=items,nextPageToken' % {'filter' : FILTER}
CREATE_URL = 'https://www.googleapis.com/drive/v3/files?fields=webViewLink' 

CACHE_MAX_AGE = 60*60*24*30 # cache set to 1 month

MIMETYPES = {
    'DOC' : 'application/vnd.google-apps.document',
    'SHEET' : 'application/vnd.google-apps.spreadsheet',
    'SLIDE' : 'application/vnd.google-apps.presentation',
    'FORM' : 'application/vnd.google-apps.form'
}

SETTINGS = {
    'LOGIN' : {
        'title' : 'Login',
        'autocomplete' : '> Login',
        'arg' : 'login',
        'icon' : ICON_ACCOUNT,
        'uid' : '0728125C-F4A9-4DB1-A28B-CD0CE0177FF2'
    },
    'LOGOUT' : {
        'title' : 'Logout',
        'autocomplete' : '> Logout',
        'arg' : 'logout',
        'icon' : ICON_EJECT,
        'uid' : '529E8958-C154-48D3-8F66-650215C38249'
    },
    'CLEAR_CACHE' : {
        'title' : 'Clear cache',
        'autocomplete' : '> Clear cache',
        'arg' : 'clear',
        'icon' : ICON_SYNC,
        'uid' : '83F6318C-5BAB-4CA5-BCC0-E9CA38E36C5F'
    },
    'SET_CACHE' : {
        'title' : 'Set cache length %s',
        'autocomplete' : '> Set cache length ',
        'arg' : 'set%s',
        'icon' : ICON_CLOCK,
        'uid' : '7C76815E-DEA3-4806-A434-1569CBADF205'
    }
}

CREATE_SETTINGS = {
    'DOC' : {
        'title' : 'New Document',
        'autocomplete' : '> New Document',
        'arg' : 'create_doc',
        'icon' : './icons/doc.png',
        'uid' : '6EA9C89F-E56A-4DD5-AF21-870869D441E6'
    },
    'SHEET' : {
        'title' : 'New Spreadsheet',
        'autocomplete' : '> New Spreadsheet',
        'arg' : 'create_sheet',
        'icon' : './icons/sheet.png',
        'uid' : 'ACAA585E-C8CE-4D64-AE64-2AD41F6CA9F5'
    },
    'SLIDE' : {
        'title' : 'New Presentation',
        'autocomplete' : '> New Presentation',
        'arg' : 'create_slide',
        'icon' : './icons/slide.png',
        'uid' : 'EB4B6437-13DB-4E65-9F7D-5BE060E37649'
    },
    'FORM' : {
        'title' : 'New Form',
        'autocomplete' : '> New Form',
        'arg' : 'create_form',
        'icon' : './icons/form.png',
        'uid' : '3D2966E3-0639-411D-8334-E1926B8626CF'
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

