'''
MCAT Meeting Coordination Assistance Tool for Django
Django settings for mcatdjango project.
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

URL_ROOT = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Calvin Root', 'root@localhost'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'mcat',
        'USER':     'mcat',
        'PASSWORD': 'mcat',
#         'ENGINE':   'django.db.backends.sqlite3',
#         'NAME':     PROJECT_ROOT+'/sqlite.db',
#         'USER':     '',
#         'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ja'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT+'/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = URL_ROOT+'/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'mcatdjango.urls'

LOGIN_REDIRECT_URL = URL_ROOT+'/'
LOGIN_URL = URL_ROOT+'/login/'
LOGOUT_URL = URL_ROOT+'/logout/'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mcatdjango.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PACKAGE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'mcat',
)



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOCALE_PATHS = (
    PROJECT_ROOT+'/mcat/locale',
    PROJECT_ROOT+'/mcatdjango/locale',
)

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = '[MCAT] '
EMAIL_USE_TLS = False

# Uncomment the next line for User Registration
# ACCOUNT_ACTIVATION_DAYS = 7
# INSTALLED_APPS = INSTALLED_APPS + ('registration',)

# Uncomment the next lines for Shibboleth IdP authentification
# USE_DJANGO_SHIBBOLETH = True
# SHIB_ATTRIBUTE_MAP = {
#     "HTTP_SHIB_IDENTITY_PROVIDER": (True, "idp"),
#     "HTTP_CN": (True, "cn"),
#     "HTTP_MAIL": (True, "email"),
#     "HTTP_GIVENNAME": (False, "first_name"),
#     "HTTP_SN": (False, "last_name"),
# }
# SHIB_USERNAME = "cn"
# SHIB_EMAIL = "email"
# SHIB_FIRST_NAME = "first_name"
# SHIB_LAST_NAME = "last_name"
# INSTALLED_APPS = INSTALLED_APPS + ('django_shibboleth',)

# Uncomment the next line for Open ID authentification
#OPENID_CREATE_USERS = True
#OPENID_UPDATE_DETAILS_FROM_SREG = True
##OPENID_UPDATE_DETAILS_FROM_AX = True
#USE_DJANGO_OPENID_AUTH = True
#AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + ('django_openid_auth.auth.OpenIDBackend',)
#INSTALLED_APPS = INSTALLED_APPS + ('django_openid_auth',)
