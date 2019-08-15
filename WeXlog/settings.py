"""
Django settings for WeXlog project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
# from distutils.sysconfig import get_python_lib
# os.environ["PATH"] += os.pathsep + get_python_lib() + '\\osgeo'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hx*but#(z9!jwy1b2o%sjv3d=k)1h1n^qu%xkwzwb8$h5o4dzf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #allauth-applications
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #internal Applications
    'users.apps.UsersConfig',
    'Profile.apps.ProfileConfig',
    'db_flatten.apps.DbFlattenConfig',
    'locations.apps.LocationsConfig',
    'enterprises.apps.EnterprisesConfig',
    'project.apps.ProjectConfig',
    'booklist.apps.BooklistConfig',
    'talenttrack.apps.TalenttrackConfig',
    'trustpassport.apps.TrustpassportConfig',
    'marketplace.apps.MarketplaceConfig',
    'payments.apps.PaymentsConfig',
    ##Django internal applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    #3rd Party Applications
    'django_countries',
    'crispy_forms',
    'django.contrib.postgres',
    'django_extensions',
    'django_messages',
    'utils',
    'phonenumber_field',
    'leaflet',
    'django_select2',
    'pinax.notifications',
    'paypal.standard.ipn',
    ]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
            #3rd party MIDDLEWARE
    'django_referrer_policy.middleware.ReferrerPolicyMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'WeXlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
#            'loaders': [
#            ('django.template.loaders.cached.Loader', [
#                'django.template.loaders.filesystem.Loader',
#                'django.template.loaders.app_directories.Loader',
#            ]),
#        ],
        },
    },
]

#all-Auth Settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False




PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]



WSGI_APPLICATION = 'WeXlog.wsgi.application'


## Web Security Headers
    ##To test use www.securityheaders.com
    ##X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True
    ##Strict Transport Security (Site must be HTTPS, HTTP rejected)
#SECURE_HSTS_SECONDS = 1800
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
    ##X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = True
    ## X-Frame-Options (DENY, WHITELIST)
X_FRAME_OPTIONS = 'DENY'
    ##django-referrer-policy (3rd party app)
REFERRER_POLICY='same-origin'
    ## Content-Security-policy (3rd party app)
CSP_DEFAULT_SRC = ("'self'",'maxcdn.bootstrapcdn.com', 'code.jquery.com',
'cdnjs.cloudflare.com')

CSP_SCRIPT_SRC = None
CSP_IMG_SRC = None
CSP_OBJECT_SRC = None
CSP_MEDIA_SRC = None
CSP_FRAME_SRC = None
CSP_FONT_SRC = None
CSP_CONNECT_SRC = None
CSP_STYLE_SRC = None
CSP_BASE_URI = None
CSP_CHILD_SRC = None
CSP_FRAME_ANCESTORS = None
CSP_FORM_ACTION = None
CSP_SANDBOX = None
CSP_REPORT_URI = None
CSP_MANIFEST_SRC = None
CSP_WORKER_SRC = None
CSP_PLUGIN_TYPES = None
CSP_REQUIRE_SRI_FOR = None
CSP_UPGRADE_INSECURE_REQUESTS = False
CSP_BLOCK_ALL_MIXED_CONTENT = False
CSP_INCLUDE_NONCE_IN = None
CSP_REPORT_ONLY = False
#CSP_EXCLUDE_URL_PREFIXES = ()
    ##cookie flags
#CSRF_COOKIE_SECURE = True
#CSRF_USE_SESSIONS = True
#CSRF_COOKIE_HTTPONLY = True
#SESSION_COOKIE_SECURE = True
#SESSION_COOKIE_SAMESITE = 'Strict'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Wexlog_1',
        'USER': 'postgres',
		'PASSWORD': 'rdf8tm1234' #MA
        #'PASSWORD': 'dJpfss41678', #JK
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#Authorisation settings
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'account/login/'
LOGIN_REDIRECT_URL = 'Profile:ProfileHome'
LOGOUT_REDIRECT_URL = 'home'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/library/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'filelibrary')

#Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# GDAL_LIBRARY_PATH = r'C:/OSGeo4W64/bin/gdal203'

#  os.environ["PATH"] += os.pathsep + BASE_DIR + '\\venv\\Lib\\site-packages\\osgeo'

#POPUP_TEMPLATE_NAME_CREATE = 'popup/create.html'
#POPUP_TEMPLATE_NAME_UPDATE = 'popup/update.html'

#FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

#Django Messages settings
DJANGO_MESSAGES_NOTIFY = False

# PayPal settings
PAYPAL_RECEIVER_EMAIL = "yourpaypalemail@example.com"
PAYPAL_TEST = True              # set to False for production

PAYPAL_SUBSCRIPTION_BUTTON_IMAGE = "images/subscribe.jpg"       # The URL of the image to be used for ‘subscription’ buttons.

PAYPAL_PRIVATE_CERT = '/path/to/paypal_private.pem'
PAYPAL_PUBLIC_CERT = '/path/to/paypal_public.pem'
PAYPAL_CERT = '/path/to/paypal_cert.pem'
PAYPAL_CERT_ID = 'get-from-paypal-website'

# path to keypair in PEM format
MY_KEYPAIR='keys/keypair.pem'

# path to merchant certificate
MY_CERT='keys/merchant.crt'

# code which Paypal assign to the certificate when you upload it
MY_CERT_ID='ASDF12345'

# path to Paypal's own certificate
PAYPAL_CERT='keys/paypal.crt'
