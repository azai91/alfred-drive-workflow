CLIENT_ID = '978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com'
CLIENT_SECRET = 'rty2NIATZfWFWSDX-XPs2usX'
SCOPE = 'https://www.googleapis.com/auth/drive.readonly'
REDIRECT_URI = 'http://localhost:1337'

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth?scope=%s&redirect_uri=%s&response_type=code&client_id=%s&access_type=offline&approval_prompt=force' % (SCOPE, REDIRECT_URI, CLIENT_ID)
TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'
FILES_URL = 'https://www.googleapis.com/drive/v2/files?orderBy=lastViewedByMeDate+desc&fields=items'

CACHE_MAX_AGE = 60*5 # cache set to 5 minutes