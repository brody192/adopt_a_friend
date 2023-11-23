from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ko3&^p3c-^^41_c#r$#s-7q+_onf543=(676g#dx#ya0_@!sji'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['adoptafriend.up.railway.app']
CSRF_TRUSTED_ORIGINS=['https://adoptafriend.up.railway.app']
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "verify_email.apps.VerifyEmailConfig",
    'main',
    'users',
    'videochat',
    'pets',
    'staff',
    'donation',
    'django_social_share',
    'chat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'adopt_a_friend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adopt_a_friend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'gbb-ad53-BD2A4cE616DCBfbb54D51gC',
        'HOST': 'monorail.proxy.rlwy.net',
        'PORT': '40606',
    }
}

# # settings.py

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'railway',
#         'USER': 'root',
#         'PASSWORD': 'adFaGFabeec-5FB16AfeBbC65dAh2bbc',
#         'HOST': 'roundhouse.proxy.rlwy.net',    # Set to the MySQL server's hostname or IP address
#         'PORT': '18063',         # MySQL default port is 3306
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nhoryybanez13@gmail.com'
EMAIL_HOST_PASSWORD = 'bxle vypt xmmd moyx'

DEFAULT_FROM_EMAIL = 'noreply<no_reply@domain.com>'

AUTH_USER_MODEL = 'users.Users'

LOGOUT_REDIRECT_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAX_RETRIES = 6

HTML_MESSAGE_TEMPLATE = "users/email.html"

#VERIFICATION_SUCCESS_TEMPLATE = "users/new_email.html"

#VERIFICATION_FAILED_TEMPLATE = "path/to/failed.html"

REQUEST_NEW_EMAIL_TEMPLATE = "users/request_new_email.html"

#LINK_EXPIRED_TEMPLATE = 'path/to/expired.html'

#NEW_EMAIL_SENT_TEMPLATE  = 'users/new_email.html'

LOGIN_URL = "login"