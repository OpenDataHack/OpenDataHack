DOMAIN = 'localhost'

ALLOWED_HOSTS = [DOMAIN]

if DOMAIN == 'localhost':
    DEBUG = True
else:
    DEBUG = False

RUNSERVER_PORT = 80